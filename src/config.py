from pathlib import Path


PROJECT_ROOT = Path(
    "/content/drive/MyDrive/LPR_Project/MD_LicensePlate_Fadiran_ITAI1378"
)

RUN_DIR = Path(
    "/content/drive/MyDrive/LPR_Project/MD_LicensePlate_Fadiran_ITAI1378/runs/detect/predict/crops/License_Plate"
)


# Demo ingestion folder
INCOMING_IMAGE_DIR = Path(
    "/content/drive/MyDrive/LPR_Inbox/incoming"
)


# Test regression images
TEST_IMAGE_DIR = PROJECT_ROOT / "data" / "test"


# Detection outputs
CROPPED_DIR = PROJECT_ROOT / "data" / "cropped"

DETECTION_METADATA_DIR = PROJECT_ROOT / "data" / "detections"


# Model
MODEL_PATH = Path(
    "/content/drive/MyDrive/YOLO_BSLN_Training/weights/best.pt"
)


# Database
DATABASE_PATH = PROJECT_ROOT / "database" / "lpr.db"

# ==========================================
# OCR SETTINGS
# ==========================================

# Minimum confidence required for the fast-path raw image (Pass 1)
OCR_CONF_PRIMARY = 0.60 

# Minimum confidence required for the sharpened fallback image (Pass 2)
OCR_CONF_FALLBACK = 0.25