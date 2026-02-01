from .dtos import PatientDataDTO, AnalysisResultDTO
from typing import Tuple

def calculate_curb65(data: PatientDataDTO) -> Tuple[int, str]:
   
    score = 0
    
    if data.confusion:
        score += 1
        
    use_urea = data.urea is not None
    if use_urea:
        if data.urea > 7:
            score += 1
            
    if data.respiratory_rate is not None and data.respiratory_rate >= 30:
        score += 1
        
    if (data.bp_systolic is not None and data.bp_systolic < 90) or \
       (data.bp_diastolic is not None and data.bp_diastolic <= 60):
        score += 1
        
    if data.age is not None and data.age >= 65:
        score += 1
        
    score_type = "CURB-65" if use_urea else "CRB-65"
    return score, score_type
