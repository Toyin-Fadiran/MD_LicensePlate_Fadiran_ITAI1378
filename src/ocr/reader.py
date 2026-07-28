import easyocr
import re

class PlateReader:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
    
    def normalize_plate(self, text):
        """Normalize license plate text by converting to uppercase and stripping all non-alphanumeric characters."""
        # \W+ matches any non-word character (equivalent to [^a-zA-Z0-9_])
        # We use a custom set to explicitly keep only letters and numbers
        return re.sub(r'[^A-Z0-9]', '', text.upper())

    def read(self, image_path):
        # image_path can just be the string path to your saved .jpg crop
        results = self.reader.readtext(image_path)

        if not results:
            return []

        plates = []
        for bbox, text, confidence in results:
            normalized_text = self.normalize_plate(text)
            
            # Optional but recommended: Filter out tiny garbage reads
            if len(normalized_text) >= 4: 
                plates.append({
                    "plate": normalized_text,
                    "confidence": confidence,
                    "bbox": bbox
                })
        
        return plates