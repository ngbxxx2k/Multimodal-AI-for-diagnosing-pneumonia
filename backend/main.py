from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import json
import io
import base64
from PIL import Image
from ai_engine.orchestrator import MedicalOrchestrator
from core.dtos import PatientDataDTO
from utils.response_helper import format_ui_response
import config
import uvicorn

app = FastAPI(title="PneumoScanAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = MedicalOrchestrator()

@app.get("/")
def health_check():
    return {"status": "ok", "message": "PneumoScanAI API đang chạy!"}

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    data: str = Form(...) 
):
    try:
        clinical_data = json.loads(data)
        vitals = clinical_data.get('vitals', {})
        labs = clinical_data.get('labs', {})
        
        def safe_float(val):
            try: return float(val)
            except: return None
                
        def safe_int(val):
            try: return int(float(val))
            except: return None

        patient_dto = PatientDataDTO(
            xray_image=None, 
            age=safe_int(vitals.get('age')),
            gender="Unknown", 
            confusion=clinical_data.get('confusion') == 'Yes',
            urea=safe_float(labs.get('urea')),
            respiratory_rate=safe_int(vitals.get('respRate')),
            bp_systolic=int(vitals.get('bp', '120/80').split('/')[0]) if '/' in vitals.get('bp', '') else None,
            bp_diastolic=int(vitals.get('bp', '120/80').split('/')[1]) if '/' in vitals.get('bp', '') else None,
            wbc=safe_float(labs.get('wbc')),
            crp=safe_float(labs.get('crp')),
            spo2=safe_float(labs.get('spo2')),
            temperature=safe_float(vitals.get('temp')),
            doctor_note=clinical_data.get('notes', '')
        )
        
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        patient_dto.xray_image = image
        
        result = orchestrator.analyze_patient(patient_dto)
        
        response_data = format_ui_response(patient_dto, result)
        
        return response_data

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)
