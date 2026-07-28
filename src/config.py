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

# Standard US plates are usually 5-7 characters, rarely 4 or 8.
MIN_PLATE_LENGTH = 4
MAX_PLATE_LENGTH = 8

# A set of normalized state names to exclude from OCR results
STATE_EXCLUSIONS = {
    "ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", "COLORADO", 
    "CONNECTICUT", "DELAWARE", "FLORIDA", "GEORGIA", "HAWAII", "IDAHO", 
    "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY", "LOUISIANA", 
    "MAINE", "MARYLAND", "MASSACHUSETTS", "MICHIGAN", "MINNESOTA", 
    "MISSISSIPPI", "MISSOURI", "MONTANA", "NEBRASKA", "NEVADA", 
    "NEWHAMPSHIRE", "NEWJERSEY", "NEWMEXICO", "NEWYORK", "NORTHCAROLINA", 
    "NORTHDAKOTA", "OHIO", "OKLAHOMA", "OREGON", "PENNSYLVANIA", 
    "RHODEISLAND", "SOUTHCAROLINA", "SOUTHDAKOTA", "TENNESSEE", "TEXAS", 
    "UTAH", "VERMONT", "VIRGINIA", "WASHINGTON", "WESTVIRGINIA", 
    "WISCONSIN", "WYOMING"
}