from pathlib import Path


# ==========================
# Project Root
# ==========================

PROJECT_ROOT = Path(
    "/content/drive/MyDrive/LPR_Project/MD_LicensePlate_Fadiran_ITAI1378"
)


# ==========================
# Model
# ==========================

MODEL_PATH = Path(
    "/content/drive/MyDrive/YOLO_BSLN_Training/weights/best.pt"
)


# ==========================
# Input Data
# ==========================

RAW_IMAGE_DIR = Path(
    "/content/drive/MyDrive/License_Plate/dataset"
)


# ==========================
# Detection Outputs
# ==========================

DATA_DIR = PROJECT_ROOT / "data"

CROPPED_DIR = DATA_DIR / "cropped"

DETECTION_METADATA_DIR = DATA_DIR / "detections"


# ==========================
# Database
# ==========================

DATABASE_PATH = PROJECT_ROOT / "database" / "lpr.db"