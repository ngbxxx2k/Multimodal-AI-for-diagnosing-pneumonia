from dataclasses import dataclass
from typing import Optional, List, Any

@dataclass
class PatientDataDTO:
    xray_image: Any 
    age: Optional[int] = None
    gender: Optional[str] = None
    confusion: bool = False
    urea: Optional[float] = None
    respiratory_rate: Optional[int] = None
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    wbc: Optional[float] = None
    crp: Optional[float] = None
    spo2: Optional[float] = None
    temperature: Optional[float] = None
    doctor_note: str = ""

@dataclass
class AnalysisResultDTO:
    unet_status: str  
    densenet_prob: float
    yolo_detections: List[Any]  
    annotated_image: Any 
    curb65_score: int
    curb65_type: str 
    lung_mask: Optional[Any] = None 
    location_text: str = "" 

@dataclass
class FinalResponseDTO:
    annotated_image: Any
    report_markdown: str
