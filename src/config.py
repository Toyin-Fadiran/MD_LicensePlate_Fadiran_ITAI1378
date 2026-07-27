from pathlib import Path


PROJECT_ROOT = Path(
    "/content/drive/MyDrive/LPR_Project/MD_LicensePlate_Fadiran_ITAI1378"
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