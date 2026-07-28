import easyocr
import re
import cv2
import numpy as np

from src.config import OCR_CONF_PRIMARY, OCR_CONF_FALLBACK, MIN_PLATE_LENGTH, MAX_PLATE_LENGTH, STATE_EXCLUSIONS

class PlateReader:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
    
    def normalize_plate(self, text):
        return re.sub(r'[^A-Z0-9]', '', text.upper())

    def preprocess(self, image_path):
        """Upscales and applies contrast stretching instead of harsh sharpening."""
        img = cv2.imread(image_path)
        if img is None: return None
        
        # 2x Upscale
        img_resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        
        # Contrast Stretching (alpha = contrast control, beta = brightness control)
        # This makes blacks blacker and whites whiter without adding structural noise
        enhanced = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
        
        return enhanced

    def read(self, image_path):
        def get_main_plate(ocr_output, min_conf, was_scaled=False):
            valid_reads = []
            for bbox, text, conf in ocr_output:
                norm = self.normalize_plate(text)
                
                if (MIN_PLATE_LENGTH <= len(norm) <= MAX_PLATE_LENGTH 
                    and norm not in STATE_EXCLUSIONS 
                    and conf >= min_conf):
                    
                    # If we upscaled by 2x in preprocessing, divide coords by 2 to match original image
                    if was_scaled:
                        corrected_bbox = [[int(x/2), int(y/2)] for x, y in bbox]
                    else:
                        corrected_bbox = [[int(x), int(y)] for x, y in bbox]
                    
                    y_coords = [point[1] for point in corrected_bbox]
                    text_height = max(y_coords) - min(y_coords)
                    
                    valid_reads.append({
                        "plate": norm,
                        "confidence": conf,
                        "bbox": corrected_bbox,
                        "height": text_height
                    })
            
            if valid_reads:
                valid_reads.sort(key=lambda x: x['height'], reverse=True)
                return [valid_reads[0]] 
            return []

        # -----------------------------------------
        # PASS 1: The Fast Path (Raw Image)
        # -----------------------------------------
        raw_results = self.reader.readtext(image_path)
        high_conf_plate = get_main_plate(raw_results, min_conf=OCR_CONF_PRIMARY, was_scaled=False)
        
        if high_conf_plate:
            return high_conf_plate

        # -----------------------------------------
        # PASS 2: The Fallback (Preprocessed Image)
        # -----------------------------------------
        processed_img = self.preprocess(image_path)
        if processed_img is None: return []
        
        enhanced_results = self.reader.readtext(processed_img)
        return get_main_plate(enhanced_results, min_conf=OCR_CONF_FALLBACK, was_scaled=True)