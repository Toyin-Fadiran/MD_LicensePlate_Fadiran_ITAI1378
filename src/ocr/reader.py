import easyocr
import re
import cv2
import numpy as np

# Import your externalized configuration variables
from src.config import OCR_CONF_PRIMARY, OCR_CONF_FALLBACK

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
        raw_results = self.reader.readtext(image_path)
        
        def get_main_plate(ocr_output, min_conf):
            valid_reads = []
            for bbox, text, conf in ocr_output:
                norm = self.normalize_plate(text)
                
                if len(norm) >= 4 and conf >= min_conf:
                    # Extract all the Y coordinates from the 4 corners of the bbox
                    y_coords = [point[1] for point in bbox]
                    
                    # Calculate the pixel height of this specific text
                    text_height = max(y_coords) - min(y_coords)
                    
                    valid_reads.append({
                        "plate": norm,
                        "confidence": conf,
                        "bbox": bbox,
                        "height": text_height
                    })
            
            # If we found valid text, sort by height (descending) and return the tallest
            if valid_reads:
                valid_reads.sort(key=lambda x: x['height'], reverse=True)
                return [valid_reads[0]] # Return as a list of 1
                
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
        
        enhanced_results = self.reader.readtext(processed_img)
        return get_main_plate(enhanced_results, min_conf=OCR_CONF_FALLBACK)