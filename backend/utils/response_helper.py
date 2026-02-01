from core.dtos import PatientDataDTO, FinalResponseDTO
from core.medical_calc import calculate_curb65
import io
import base64

def format_ui_response(patient_dto: PatientDataDTO, result: FinalResponseDTO):
    buffered = io.BytesIO()
    result.annotated_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    img_data_url = f"data:image/png;base64,{img_str}"
    
    report = result.report_markdown
    
    diagnosis = "Phát hiện Viêm phổi" if "High probability" in report or result.pneumonia_prob > 50 else "Bình thường / Nguy cơ thấp"
    if "Indeterminate" in report:
        diagnosis = "Kết quả không xác định"
        
    severity = "Nguy cơ thấp"
    if "High Risk" in report:
        severity = "Nguy cơ cao"
    elif "Moderate Risk" in report:
        severity = "Nguy cơ trung bình"
        
    curb_score, _ = calculate_curb65(patient_dto)
    
    criteria = []
    if patient_dto.confusion: criteria.append("Mất ý thức / Lú lẫn")
    if patient_dto.urea and patient_dto.urea > 7: criteria.append("Urea > 7 mmol/L")
    if patient_dto.respiratory_rate and patient_dto.respiratory_rate >= 30: criteria.append("Nhịp thở >= 30")
    if (patient_dto.bp_systolic and patient_dto.bp_systolic < 90) or (patient_dto.bp_diastolic and patient_dto.bp_diastolic <= 60): criteria.append("Huyết áp thấp")
    if patient_dto.age is not None and patient_dto.age >= 65: criteria.append("Tuổi >= 65")
    
    recommendation = "Đề nghị hội chẩn lâm sàng."
    if "## 3. Kết luận & Khuyến nghị" in report:
        try:
            parts = report.split("## 3. Kết luận & Khuyến nghị")
            if len(parts) > 1:
                recommendation = parts[1].replace("(Final Recommendation)", "").strip()
        except:
            pass
            
    location = getattr(result, 'location_text', 'Vùng không xác định')
    
    confidence = getattr(result, 'pneumonia_prob', 0.0)
    
    return {
        "diagnosis": diagnosis,
        "severity": severity,
        "curbScore": curb_score,
        "criteria": criteria,
        "recommendation": recommendation,
        "confidence": confidence,
        "location": location,
        "fullReport": result.report_markdown,
        "annotatedImage": img_data_url
    }
