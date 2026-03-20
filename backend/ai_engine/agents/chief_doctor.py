import json
from ai_engine.llm_client import LLMClient
from ai_engine.prompts import CHIEF_DOCTOR_SYSTEM_PROMPT

class ChiefDoctorAgent:
    def __init__(self):
        self.client = LLMClient()

    def conclude(self, patient_data, densenet_prob, curb_score, curb_type) -> str:
        """
        Tổng hợp các thông tin y khoa để đưa ra chẩn đoán và hướng xử trí cuối cùng.
        """
        input_data = {
            "densenet_prob": round(densenet_prob, 2),
            "curb_score": curb_score,
            "curb_type": curb_type,
            "patient_info": {
                "age": patient_data.age,
                "gender": patient_data.gender,
                "confusion": patient_data.confusion,
                "urea": patient_data.urea,
                "respiratory_rate": patient_data.respiratory_rate,
                "bp_systolic": patient_data.bp_systolic,
                "bp_diastolic": patient_data.bp_diastolic,
                "wbc": patient_data.wbc,
                "crp": patient_data.crp,
                "spo2": patient_data.spo2,
                "temperature": patient_data.temperature,
                "doctor_note": patient_data.doctor_note
            }
        }
        
        input_json = json.dumps(input_data, indent=2, ensure_ascii=False)
        return self.client.generate_text(CHIEF_DOCTOR_SYSTEM_PROMPT, input_json)
