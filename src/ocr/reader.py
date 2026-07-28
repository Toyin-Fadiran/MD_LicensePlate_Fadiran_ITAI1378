import re
import cv2
import numpy as np
import logging
from paddleocr import PaddleOCR

# Force PaddleOCR to stay quiet
logging.getLogger("ppocr").setLevel(logging.ERROR)

from src.config import OCR_CONF_PRIMARY, OCR_CONF_FALLBACK, MIN_PLATE_LENGTH, MAX_PLATE_LENGTH, STATE_EXCLUSIONS

class PlateReader:
    def __init__(self):
        self.reader = PaddleOCR(use_angle_cls=False, lang='en')
        
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
        raw_results = self.reader.ocr(image_path)
        
        # 1. Added was_scaled back as an argument
        def get_main_plate(ocr_output, min_conf, was_scaled=False):
            if not ocr_output or not ocr_output[0]:
                return []
                
            valid_reads = []
            
            for line in ocr_output[0]:
                raw_bbox = line[0]        
                text = line[1][0]     
                conf = line[1][1]     
                
                norm = self.normalize_plate(text)
                
                if (MIN_PLATE_LENGTH <= len(norm) <= MAX_PLATE_LENGTH 
                    and norm not in STATE_EXCLUSIONS 
                    and conf >= min_conf):
                    
                    # 2. Restored the scaling math!
                    if was_scaled:
                        bbox = [[int(x/2), int(y/2)] for x, y in raw_bbox]
                    else:
                        bbox = [[int(x), int(y)] for x, y in raw_bbox]
                    
                    y_coords = [point[1] for point in bbox]
                    text_height = max(y_coords) - min(y_coords)
                    
                    valid_reads.append({
                        "plate": norm,
                        "confidence": conf,
                        "bbox": bbox,
                        "height": text_height
                    })
            
            if valid_reads:
                valid_reads.sort(key=lambda x: x['height'], reverse=True)
                return [valid_reads[0]] 
                
            return []

        # -----------------------------------------
        # PASS 1: The Fast Path
        # -----------------------------------------
        # 3. Passed was_scaled=False
        high_conf_plate = get_main_plate(raw_results, min_conf=OCR_CONF_PRIMARY, was_scaled=False)
        if high_conf_plate:
            return high_conf_plate

        # -----------------------------------------
        # PASS 2: The Fallback
        # -----------------------------------------
        processed_img = self.preprocess(image_path)
        if processed_img is None: return []
        
        enhanced_results = self.reader.ocr(processed_img)
        
        # 4. Passed was_scaled=True
        return get_main_plate(enhanced_results, min_conf=OCR_CONF_FALLBACK, was_scaled=True)