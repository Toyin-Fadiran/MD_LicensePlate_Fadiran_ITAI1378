# AI Usage Log
**Project:** Automated License Plate Recognition (ALPR) System

---

## Entry 1: Overcoming OCR Limitations with Pre-Processing
* **Date and tool used:** 2026-07-08 | Gemini (LLM)  
* **What you asked, or the problem you had:** I was exploring risk mitigations for the CV pipeline project. I initially assumed that because EasyOCR uses a deep learning architecture, it would automatically handle the low-resolution and degraded bounding box crops outputted by YOLOv11.
* **What the AI suggested:** The AI clarified that while EasyOCR is robust for "text in the wild," it cannot invent missing pixel data from a 40x15 pixel crop. It suggested writing an OpenCV pre-processing script utilizing grayscale conversion, cubic upscaling, bilateral filtering, and adaptive thresholding to clean the YOLO crops before passing them to the OCR engine.
* **What you learned:** I learned the exact mechanical distinction between what modern deep learning OCR handles natively (like curved text) versus where traditional image matrix manipulations are still absolutely required (pixel density and contrast correction).
* **How you applied it in your project:** I added this OpenCV pre-processing step as the primary mitigation strategy for my highest-probability risk in the README, and incorporated OpenCV into the technical pipeline for the Make It Yours phase.

---

### Entry 2: Multi-Plate Image Cropping & Suffix Indexing
* **Date & Tool Used:** 2026-07-16 | Gemini (LLM)  
* **Problem / What I Asked:**  
  * When running YOLO11n spatial detection over parking lot images containing multiple vehicles, my cropping script was overwriting crops or throwing filename collision errors when saving dynamically generated bounding boxes.  
* **What the AI Suggested:**  
  * The AI suggested implementing an enumerated loop over `result.boxes` to append an ordered index suffix (`f"{image_path.stem}_plate_{i+1}.jpg"`) and storing the corresponding spatial coordinates (`x1, y1, x2, y2`) inside an array of dictionaries written to a per-image JSON file.  
* **What I Learned:**  
  * I learned how to decouple object detection inference from downstream recognition by using standardized filesystem naming conventions and structured JSON metadata as a bridge between Jupyter notebooks.  
* **How I Applied It:**  
  * I integrated the dynamic cropping loop and JSON metadata exporter directly into `01_detection.ipynb`, allowing Notebook 2 to cleanly trace every individual crop back to its original source image without data loss.

---

### Entry 3: OCR Accuracy Troubleshooting & Model Pivot
* **Date & Tool Used:** 2026-07-21 | Gemini (LLM)  
* **Problem / What I Asked:**  
  * The original Blueprint promised to use EasyOCR, but during SIT/UAT testing, CPU-bound EasyOCR consistently misread alphanumeric characters on real-world license plate crops—even after applying OpenCV preprocessing (grayscale, cubic upscaling, adaptive thresholding).  
* **What the AI Suggested:**  
  * The AI explained that EasyOCR's limitations stem from model architecture capacity rather than image contrast, and suggested pivoting to a GPU-accelerated deep learning OCR model (PaddleOCR-GPU) while adding an alphanumeric string sanitization loop.  
* **What I Learned:**  
  * I learned that extensive visual preprocessing cannot compensate for an OCR engine's architectural bottlenecks, and that professional engineering requires pivoting away from Blueprint assumptions when real-world performance fails.  
* **How I Applied It:**  
  * I documented the engineering justification for the model swap in our "What Changed" analysis, replaced EasyOCR with `PaddleOCR-GPU` inside `02_ocr_database.ipynb`, and built a custom text-sanitization loop that strips 50 normalized US state names before SQL database queries.

---
### Entry 4: Free-Tier Cloud GPU Training Timeouts
* **Date & Tool Used:** 2026-07-24 | Gemini (LLM)  
* **Problem / What I Asked:**  
  * While training our YOLO11n spatial detector on 10,125 Roboflow images using `epochs=100`, Google Colab's free-tier GPU session timed out after ~2 hours, disconnecting the runtime before weights could be saved.  
* **What the AI Suggested:**  
  * The AI suggested scaling down the training hyperparameters to `epochs=50`, `imgsz=640`, and `batch=16`, explaining that a lightweight single-stage detector converges sufficiently on ~10k images well within the 2-hour free-tier window.  
* **What I Learned:**  
  * I learned how to balance convergence targets against infrastructure and budget constraints, discovering that 50 epochs is the sweet spot for YOLO11n on this dataset size.  
* **How I Applied It:**  
  * I updated `data.yaml` training configurations to `epochs=50` under the run name `"license_plate_baseline_50"`, successfully training the model to an `mAP@0.5` of ~0.97 without hitting Colab timeout constraints.

---

### Entry 7: Alphanumeric State-Name Sanitization for OCR
* **Date & Tool Used:** 2026-07-26 | Gemini (LLM)  
* **Problem / What I Asked:**  
  * Even after upgrading to PaddleOCR-GPU, raw OCR text extraction from cropped plates frequently included printed US state names (e.g., `"TEXAS"`, `"CALIFORNIA"`, `"ALABAMA"`) along with the actual license plate number, which caused relational database queries to fail.  
* **What the AI Suggested:**  
  * The AI suggested writing a programmatic Python sanitization function using a normalized array of all 50 US state names (and common abbreviations) to strip regional identifiers, whitespace, and special characters from the OCR string before passing it downstream.  
* **What I Learned:**  
  * I learned that raw optical character recognition output must be treated as untrusted, noisy input that requires domain-specific text parsing and regex cleaning before it can be used as a database key.  
* **How I Applied It:**  
  * I built a text sanitization pipeline inside `02_ocr_database.ipynb` that automatically filters out state names and non-alphanumeric characters, ensuring only clean plate IDs are queried against the database.

---
