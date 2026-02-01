import json
from ai_engine.llm_client import LLMClient
from ai_engine.prompts import RADIOLOGIST_SYSTEM_PROMPT

class RadiologistAgent:
    def __init__(self):
        self.client = LLMClient()

    def analyze(self, densenet_prob: float, detections: list) -> str:
        """
        Phân tích dữ liệu hình ảnh để đưa ra mô tả phát hiện X quang.
        
        Đầu vào:
            densenet_prob: float (0-100)
            detections: danh sách dict (từ YOLO)
        Đầu ra:
            str (Mô tả văn bản)
        """
        input_data = {
            "densenet_probability": f"{densenet_prob:.2f}%",
            "yolo_detections": detections
        }
        
        input_json = json.dumps(input_data, indent=2)
        return self.client.generate_text(RADIOLOGIST_SYSTEM_PROMPT, input_json)
