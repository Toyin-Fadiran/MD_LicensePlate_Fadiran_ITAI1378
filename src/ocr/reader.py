import easyocr
import re
import cv2
import numpy as np

# Import your externalized configuration variables (Fallback removed)
from src.config import OCR_CONF_PRIMARY, MIN_PLATE_LENGTH, MAX_PLATE_LENGTH, STATE_EXCLUSIONS

class PlateReader:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
    
    def normalize_plate(self, text):
        """Normalize license plate text by converting to uppercase and stripping all non-alphanumeric characters."""
        return re.sub(r'[^A-Z0-9]', '', text.upper())

    def preprocess(self, image_path):
        """Upscales and sharpens the image to resolve edge-case characters."""
        img = cv2.imread(image_path)
        if img is None: return None
        
        img_resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        return cv2.filter2D(gray, -1, kernel)

    def read(self, image_path):
        # -----------------------------------------
        # MANDATORY PREPROCESSING FOR ALL IMAGES
        # -----------------------------------------
        processed_img = self.preprocess(image_path)
        
        # Failsafe if the image didn't load properly
        if processed_img is None: 
            return []
            
        # Pass the preprocessed OpenCV array directly to EasyOCR
        results = self.reader.readtext(processed_img)
        
        def get_main_plate(ocr_output, min_conf):
            valid_reads = []
            for bbox, text, conf in ocr_output:
                norm = self.normalize_plate(text)
                
                # 1. Length Check
                # 2. Exclusion Check
                # 3. Confidence Check
                if (MIN_PLATE_LENGTH <= len(norm) <= MAX_PLATE_LENGTH 
                    and norm not in STATE_EXCLUSIONS 
                    and conf >= min_conf):
                    
                    y_coords = [point[1] for point in bbox]
                    text_height = max(y_coords) - min(y_coords)
                    
                    valid_reads.append({
                        "plate": norm,
                        "confidence": conf,
                        "bbox": bbox,
                        "height": text_height
                    })
            
            # Sort whatever survived by height
            if valid_reads:
                valid_reads.sort(key=lambda x: x['height'], reverse=True)
                return [valid_reads[0]] 
                
            return []

        # Return the single best plate using your primary confidence threshold
        return get_main_plate(results, min_conf=OCR_CONF_PRIMARY)