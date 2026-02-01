from ai_engine.vision_models import VisionEngine
from ai_engine.agents.radiologist import RadiologistAgent
from ai_engine.agents.lab_specialist import LabSpecialistAgent
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
        self.radiologist = RadiologistAgent()
        self.lab_specialist = LabSpecialistAgent()
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

        if pneumonia_prob > 80:
            yolo_conf = 0.10
        else:
            yolo_conf = 0.25
            
        _, detections = self.vision.detect_abnormalities(original_image, conf_threshold=yolo_conf)
        
        from utils.image_processing import get_lesion_location_text
        
        overlay = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)
        
        if mask is not None:
             colored_mask = np.zeros_like(overlay)
             colored_mask[:, :, 1] = mask * 100 
             overlay = cv2.addWeighted(overlay, 1.0, colored_mask, 0.3, 0)

        primary_location = "Không xác định"
        locations_found = []

        for det in detections:
            box = det['box'] 
            conf = det['conf']
            mode = det['mode']
            
            x1, y1, x2, y2 = map(int, box)
            location_text = get_lesion_location_text([x1, y1, x2, y2], mask)
            locations_found.append(location_text)
            
            color = (0, 255, 0) if "High" in mode else (0, 255, 255) 
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, 2)
            
            label = f"{conf:.2f}"
            (w_text, h_text), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(overlay, (x1, y1 - 20), (x1 + w_text, y1), color, -1)
            cv2.putText(overlay, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)

        annotated_img_pil = Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
        
        if locations_found:
            primary_location = locations_found[0] 
            
        enriched_detections = []
        for i, det in enumerate(detections):
            loc = locations_found[i] if i < len(locations_found) else "Không xác định"
            enriched_detections.append({**det, "label": f"{det['label']} at {loc}"})
            
        rad_report = self.radiologist.analyze(pneumonia_prob, enriched_detections)
        
        curb_score, curb_type = calculate_curb65(patient_data)
        lab_report = self.lab_specialist.analyze(patient_data, curb_score, curb_type)
        
        final_markdown = self.chief.conclude(rad_report, lab_report, patient_data.doctor_note)
        
        response = FinalResponseDTO(
            annotated_image=annotated_img_pil,
            report_markdown=final_markdown
        )
        response.location_text = primary_location
        response.pneumonia_prob = pneumonia_prob
        
        return response
