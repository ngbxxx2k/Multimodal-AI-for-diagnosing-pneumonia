from ai_engine.vision_models import VisionEngine
from ai_engine.agents.chief_doctor import ChiefDoctorAgent

from core.dtos import PatientDataDTO, AnalysisResultDTO, FinalResponseDTO
from core.medical_calc import calculate_curb65
from utils.image_processing import calculate_mask_area_ratio, count_blobs, crop_lung_region
import io
import base64
from PIL import Image
import numpy as np
import cv2

class MedicalOrchestrator:
    def __init__(self):
        self.vision = VisionEngine()
        self.chief = ChiefDoctorAgent()

    def analyze_patient(self, patient_data: PatientDataDTO) -> FinalResponseDTO:
        original_image = patient_data.xray_image
        
        unet_status = "SUCCESS"
        mask = None
        try:
            mask = self.vision.predict_mask(original_image)
            
            mask_ratio = calculate_mask_area_ratio(mask)
            blobs = count_blobs(mask)
            
            if mask_ratio < 0.1 or blobs < 2:
                unet_status = "FALLBACK"
                processed_image = original_image
            else:
                processed_image_np = crop_lung_region(np.array(original_image), mask)
                processed_image = Image.fromarray(processed_image_np)
                
        except Exception as e:
            print(f"U-Net Error: {e}")
            unet_status = "FALLBACK"
            processed_image = original_image
            mask = np.zeros((np.array(original_image).shape[0], np.array(original_image).shape[1]), dtype=np.uint8)

        pneumonia_prob = self.vision.predict_pneumonia_prob(processed_image)

        overlay = cv2.cvtColor(np.array(processed_image), cv2.COLOR_RGB2BGR)

        try:
            heatmap = self.vision.generate_gradcam_heatmap(processed_image)
            if heatmap is not None:
                heatmap_resized = cv2.resize(heatmap, (processed_image.size[0], processed_image.size[1]))
                heatmap_uint8 = np.uint8(255 * heatmap_resized)
                colored_heatmap = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
                
                alpha = 0.4
                # Apply full Grad-CAM heatmap over image
                overlay = cv2.addWeighted(overlay, 1 - alpha, colored_heatmap, alpha, 0)
        except Exception as e:
            print(f"GradCAM Error: {e}")

        annotated_img_pil = Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
        
        curb_score, curb_type = calculate_curb65(patient_data)
        
        final_markdown = self.chief.conclude(patient_data, pneumonia_prob, curb_score, curb_type)
        
        response = FinalResponseDTO(
            annotated_image=annotated_img_pil,
            report_markdown=final_markdown
        )
        response.pneumonia_prob = pneumonia_prob
        
        return response
