import easyocr
import re
import cv2
import numpy as np

# Import the new exclusion rules
from src.config import OCR_CONF_PRIMARY, OCR_CONF_FALLBACK, MIN_PLATE_LENGTH, MAX_PLATE_LENGTH, STATE_EXCLUSIONS

class PlateReader:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
    
    def normalize_plate(self, text):
        return re.sub(r'[^A-Z0-9]', '', text.upper())

    def preprocess(self, image_path):
        img = cv2.imread(image_path)
        if img is None: return None
        
        img_resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        return cv2.filter2D(gray, -1, kernel)

    def read(self, image_path):
        raw_results = self.reader.readtext(image_path)
        
        def get_main_plate(ocr_output, min_conf):
            valid_reads = []
            for bbox, text, conf in ocr_output:
                norm = self.normalize_plate(text)
                
                # 1. Length Check: Drops Strings (> 8 chars)
                # 2. Exclusion Check: Drops State Names
                # 3. Confidence Check: Ensures decent OCR reads
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
            
            # Now sort whatever survived the gauntlet by height
            if valid_reads:
                valid_reads.sort(key=lambda x: x['height'], reverse=True)
                return [valid_reads[0]] 
                
            return []

        # PASS 1: The Fast Path
        high_conf_plate = get_main_plate(raw_results, min_conf=OCR_CONF_PRIMARY)
        if high_conf_plate:
            return high_conf_plate

        # PASS 2: The Fallback
        processed_img = self.preprocess(image_path)
        if processed_img is None: return []
        
        enhanced_results = self.reader.readtext(processed_img)
        return get_main_plate(enhanced_results, min_conf=OCR_CONF_FALLBACK)