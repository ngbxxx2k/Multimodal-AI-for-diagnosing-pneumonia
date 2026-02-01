import torch
import numpy as np
import cv2
from PIL import Image
from ultralytics import YOLO
from keras.models import load_model
import segmentation_models_pytorch as smp
import config

class VisionEngine:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.unet = self._load_unet()
        self.densenet = self._load_densenet()
        self.yolo = self._load_yolo()
        
    def _load_unet(self):
        try:
            unet = smp.Unet(encoder_name="resnet34", in_channels=3, classes=1).to(self.device)
            state_dict = torch.load(config.UNET_PATH, map_location=self.device)
            unet.load_state_dict(state_dict, strict=False)
            unet.eval()
            print(f"✅ U-Net loaded successfully from {config.UNET_PATH}")
            return unet
        except Exception as e:
            print(f"Error loading U-Net from {config.UNET_PATH}: {e}")
            return None

    def _load_densenet(self):
        try:
            model = load_model(config.DENSENET_PATH)
            print(f"✅ DenseNet loaded successfully from {config.DENSENET_PATH}")
            return model
        except Exception as e:
            print(f"Error loading DenseNet from {config.DENSENET_PATH}: {e}")
            return None

    def _load_yolo(self):
        try:
            model = YOLO(config.YOLO_PATH)
            print(f"✅ YOLO loaded successfully from {config.YOLO_PATH}")
            return model
        except Exception as e:
            print(f"Error loading YOLO from {config.YOLO_PATH}: {e}")
            return None

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
        mask_resized = cv2.resize(mask_np, original_size, interpolation=cv2.INTER_NEAREST)
        return mask_resized

    def predict_pneumonia_prob(self, image: Image.Image):
        if self.densenet is None:
            raise RuntimeError("DenseNet model not loaded")
            
        target_size = (224, 224)
        img_resized = image.resize(target_size).convert("RGB")
        img_np = np.array(img_resized) / 255.0
        img_batch = np.expand_dims(img_np, axis=0)
        
        pred = self.densenet.predict(img_batch)
        if pred.shape[1] == 1:
            prob = float(pred[0][0])
        else:
            prob = float(pred[0][1]) if pred.shape[1] > 1 else float(pred[0][0])
            
        return prob * 100.0

    def detect_abnormalities(self, image: Image.Image, conf_threshold: float = 0.25):
        if self.yolo is None:
            raise RuntimeError("YOLO model not loaded")
            
        results = self.yolo.predict(image, conf=conf_threshold, iou=0.45, verbose=False)[0]
        
        detections = []
        for box in results.boxes:
            b = box.xyxy[0].tolist() 
            c = float(box.conf)
            cls = int(box.cls)
            label = results.names[cls]
            detections.append({
                "box": b,
                "conf": c,
                "label": label,
                "mode": f"Conf {conf_threshold}"
            })
            
        return image, detections
