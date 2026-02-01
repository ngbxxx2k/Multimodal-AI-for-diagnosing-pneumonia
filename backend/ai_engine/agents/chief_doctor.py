import json
from ai_engine.llm_client import LLMClient
from ai_engine.prompts import CHIEF_DOCTOR_SYSTEM_PROMPT

class ChiefDoctorAgent:
    def __init__(self):
        self.client = LLMClient()

    def conclude(self, radiology_report: str, lab_report: str, doctor_note: str) -> str:
        """
        Tổng hợp các báo cáo thành một báo cáo y tế markdown cuối cùng.
        """
        input_data = {
            "radiology_report": radiology_report,
            "lab_report": lab_report,
            "doctor_note": doctor_note
        }
        
        input_json = json.dumps(input_data, indent=2)
        return self.client.generate_text(CHIEF_DOCTOR_SYSTEM_PROMPT, input_json)
