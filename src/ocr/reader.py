import easyocr


class PlateReader:

    def __init__(self):

        self.reader = easyocr.Reader(['en'])

    
    def normalize_plate(self, text):
        """Normalize license plate text by converting to uppercase and removing spaces/hyphens."""
        return (
            text
            .upper()
            .replace(" ", "")
            .replace("-", "")
        )


    def read(self, image):

        results = self.reader.readtext(image)


        if not results:
            return []

        # EasyOCR returns: [(bbox, text, confidence), ...]
        # Process all detected plates, not just the first one
        plates = []
        for bbox, text, confidence in results:
            normalized_text = self.normalize_plate(text)
            plates.append({
                "plate": normalized_text,
                "confidence": confidence,
                "bbox": bbox
            })
        
        return plates