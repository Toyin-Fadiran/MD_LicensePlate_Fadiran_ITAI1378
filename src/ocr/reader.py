import re
import cv2
import numpy as np
import logging # <-- 1. Add this import
from paddleocr import PaddleOCR

# 2. Add this line to force PaddleOCR to stay quiet
logging.getLogger("ppocr").setLevel(logging.ERROR)

from src.config import OCR_CONF_PRIMARY, OCR_CONF_FALLBACK, MIN_PLATE_LENGTH, MAX_PLATE_LENGTH, STATE_EXCLUSIONS

class PlateReader:
    def __init__(self):
        # 3. Remove 'show_log=False' from this line
        self.reader = PaddleOCR(use_angle_cls=False, lang='en')
        
    # ... [The rest of your class stays exactly the same] ...
    
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
        # PaddleOCR handles file paths directly just like EasyOCR
        raw_results = self.reader.ocr(image_path, cls=False)
        
        def get_main_plate(ocr_output, min_conf):
            # Failsafe if PaddleOCR finds absolutely nothing
            if not ocr_output or not ocr_output[0]:
                return []
                
            valid_reads = []
            
            # PaddleOCR returns data in results[0] as: [[bbox], ['text', confidence]]
            for line in ocr_output[0]:
                bbox = line[0]        # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                text = line[1][0]     # The extracted string
                conf = line[1][1]     # The confidence score
                
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

        # -----------------------------------------
        # PASS 1: The Fast Path
        # -----------------------------------------
        high_conf_plate = get_main_plate(raw_results, min_conf=OCR_CONF_PRIMARY)
        if high_conf_plate:
            return high_conf_plate

        # -----------------------------------------
        # PASS 2: The Fallback
        # -----------------------------------------
        processed_img = self.preprocess(image_path)
        if processed_img is None: return []
        
        # PaddleOCR natively accepts OpenCV numpy arrays, so we can pass it right in
        enhanced_results = self.reader.ocr(processed_img, cls=False)
        return get_main_plate(enhanced_results, min_conf=OCR_CONF_FALLBACK)