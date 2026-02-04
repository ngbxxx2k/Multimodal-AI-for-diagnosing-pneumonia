import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UNET_PATH = os.getenv("UNET_PATH", os.path.join("model_ai", "best_lung_unet.pth"))
DENSENET_PATH = os.getenv("DENSENET_PATH", os.path.join("model_ai", "best_binary_xray_recall98.keras"))
YOLO_PATH = os.getenv("YOLO_PATH", os.path.join("model_ai", "best_RSNA_HIGH_LR.pt"))

PNEUMONIA_THRES_HIGH = 80.0
YOLO_CONF_HIGH = 0.10
YOLO_CONF_LOW = 0.2
