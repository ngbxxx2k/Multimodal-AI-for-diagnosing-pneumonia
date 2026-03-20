import torch
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.densenet import preprocess_input
import segmentation_models_pytorch as smp
import config


class VisionEngine:

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.unet = self._load_unet()
        self.conv_model = None
        self.classifier_model = None
        self.densenet = self._load_densenet()

    # =============================
    # LOAD MODELS
    # =============================

    def _load_unet(self):

        try:
            unet = smp.Unet(
                encoder_name="resnet34",
                in_channels=3,
                classes=1
            ).to(self.device)

            state_dict = torch.load(
                config.UNET_PATH,
                map_location=self.device
            )

            unet.load_state_dict(state_dict, strict=False)
            unet.eval()

            print(f"U-Net loaded successfully from {config.UNET_PATH}")

            return unet

        except Exception as e:

            print(f"Error loading U-Net: {e}")

            return None

    def _load_densenet(self):

        try:

            model = load_model(config.DENSENET_PATH)

            print(f"DenseNet loaded successfully from {config.DENSENET_PATH}")
            self._init_gradcam_models(model)

            return model

        except Exception as e:

            print(f"Error loading DenseNet: {e}")

            return None

    def _init_gradcam_models(self, model):
        try:
            base_model = model.get_layer("densenet121")
            last_conv_layer = base_model.get_layer("conv5_block16_concat")

            self.conv_model = tf.keras.Model(
                inputs=base_model.input,
                outputs=last_conv_layer.output
            )

            classifier_input = tf.keras.Input(shape=last_conv_layer.output.shape[1:])
            x = classifier_input
            x = model.layers[2](x)  # GlobalAveragePooling
            x = model.layers[3](x)  # BatchNorm
            x = model.layers[4](x)  # Dense
            x = model.layers[5](x)  # Dropout
            output = model.layers[6](x)  # Sigmoid

            self.classifier_model = tf.keras.Model(classifier_input, output)
            print("GradCAM sub-models initialized successfully")
        except Exception as e:
            print(f"Error initializing GradCAM sub-models: {e}")
            self.conv_model = None
            self.classifier_model = None



    # =============================
    # U-NET SEGMENTATION
    # =============================

    def predict_mask(self, image: Image.Image):

        if self.unet is None:
            raise RuntimeError("U-Net model not loaded")

        target_size = (256, 256)
        original_size = image.size

        img_resized = image.resize(target_size).convert("RGB")
        img_np = np.array(img_resized) / 255.0

        img_np = np.transpose(img_np, (2, 0, 1))

        img_tensor = torch.from_numpy(img_np).unsqueeze(0).float().to(self.device)

        with torch.no_grad():

            output = self.unet(img_tensor)

            pred = torch.sigmoid(output) > 0.5

        mask_np = pred.squeeze().cpu().numpy().astype(np.uint8) * 255

        mask_resized = cv2.resize(
            mask_np,
            original_size,
            interpolation=cv2.INTER_NEAREST
        )

        return mask_resized

    # =============================
    # DENSENET CLASSIFICATION
    # =============================

    def predict_pneumonia_prob(self, image: Image.Image):

        if self.densenet is None:
            raise RuntimeError("DenseNet model not loaded")

        target_size = (224, 224)

        # PIL -> numpy RGB
        img_resized = image.resize(target_size).convert("RGB")

        img_np = np.array(img_resized).astype(np.float32)

        # DenseNet preprocessing
        img_np = preprocess_input(img_np)

        img_batch = np.expand_dims(img_np, axis=0)

        pred = self.densenet.predict(img_batch, verbose=0)

        prob = float(pred[0][0])

        return prob * 100.0

    # =============================
    # GRAD-CAM GENERATION
    # =============================

    def generate_gradcam_heatmap(self, image: Image.Image):

        if self.conv_model is None or self.classifier_model is None:
            raise RuntimeError("GradCAM sub-models not loaded")

        target_size = (224, 224)
        img_resized = image.resize(target_size).convert("RGB")
        img_np = np.array(img_resized).astype(np.float32)
        img_np = preprocess_input(img_np)
        img_batch = np.expand_dims(img_np, axis=0)

        with tf.GradientTape() as tape:
            conv_outputs = self.conv_model(img_batch)
            tape.watch(conv_outputs)
            preds = self.classifier_model(conv_outputs)
            loss = preds[:, 0]

        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0)
        
        max_val = tf.reduce_max(heatmap)
        if max_val > 0:
            heatmap /= max_val

        return heatmap.numpy()