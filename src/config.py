from pathlib import Path

# Project root
PROJECT_ROOT = Path("/content/drive/MyDrive/LPR_Project")


# Existing trained model
MODEL_PATH = Path(
    "/content/drive/MyDrive/YOLO_BSLN_Training/weights/best.pt"
)


# Existing raw images
RAW_IMAGE_DIR = Path(
    "/content/drive/MyDrive/License_Plate/dataset"
)


# Future outputs from detection stage
CROPPED_IMAGE_DIR = PROJECT_ROOT / "data" / "cropped"

DETECTION_METADATA_DIR = PROJECT_ROOT / "data" / "detections"
