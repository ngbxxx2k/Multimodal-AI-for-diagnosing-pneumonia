import json
from ai_engine.llm_client import LLMClient
from ai_engine.prompts import LAB_SPECIALIST_SYSTEM_PROMPT
from core.dtos import PatientDataDTO

class LabSpecialistAgent:
    def __init__(self):
        self.client = LLMClient()

    def analyze(self, patient_data: PatientDataDTO, curb_score: int, curb_type: str) -> str:
        """
        Phân tích dữ liệu phòng xét nghiệm lâm sàng để lập báo cáo phòng xét nghiệm sử dụng CURB-65/CRB-65 đã được tính toán trước.
        """
        input_data = {
            "age": patient_data.age,
            "confusion": patient_data.confusion,
            "respiratory_rate": patient_data.respiratory_rate,
            "bp_systolic": patient_data.bp_systolic,
            "bp_diastolic": patient_data.bp_diastolic,
            "urea": patient_data.urea,
            "wbc": patient_data.wbc,
            "crp": patient_data.crp,
            "spo2": patient_data.spo2,
            "temperature": patient_data.temperature,
            "calculated_score": {
                "type": curb_type,
                "score": curb_score,
                "meaning": f"{curb_type} Score = {curb_score}"
            }
        }
        
        input_json = json.dumps(input_data, indent=2)
        return self.client.generate_text(LAB_SPECIALIST_SYSTEM_PROMPT, input_json)
