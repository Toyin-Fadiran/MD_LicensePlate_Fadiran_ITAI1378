from pathlib import Path


PROJECT_ROOT = Path(
    "/content/drive/MyDrive/LPR_Project/MD_LicensePlate_Fadiran_ITAI1378"
)

RUN_DIR = Path(
    "/content/drive/MyDrive/LPR_Project/MD_LicensePlate_Fadiran_ITAI1378/runs/detect/predict/crops/License_Plate"
)

INCOMING_IMAGE_DIR = "/content/drive/MyDrive/LPR_Inbox/incoming"

# Test regression images
TEST_IMAGE_DIR = PROJECT_ROOT / "data" / "test"


# Detection outputs
CROPPED_DIR = PROJECT_ROOT / "data" / "cropped"

DETECTION_METADATA_DIR = PROJECT_ROOT / "data" / "detections"


# Model
MODEL_PATH = Path(
    "/content/drive/MyDrive/YOLO_BSLN_Training/weights/best.pt"
)


CSV_FILE_PATH = PROJECT_ROOT / "authorized_list.csv"

# Database
DATABASE_PATH = PROJECT_ROOT / "db_data" / "lpr.db"

# ==========================================
# OCR SETTINGS
# ==========================================


# Require high certainty for the raw image to bypass preprocessing
OCR_CONF_PRIMARY = 0.90 

# Require decent certainty for the final preprocessed attempt
OCR_CONF_FALLBACK = 0.40

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