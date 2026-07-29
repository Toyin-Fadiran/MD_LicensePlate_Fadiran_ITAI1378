# 🚗 License Plate Detection System

## Team Members
- **Oluwatoyin Fadiran**

## Project Tier
**Tier 1 --> Tier 2 (Multi-component System):** This project qualifies as a Tier 1 to Tier 2 system because it integrates a YOLOv11 object detection model for localization with an advanced deep learning text recognition framework (EasyOCR) to build a computer vision pipeline.

## Problem Statement
Manual vehicle logging and security monitoring in access-controlled environments, such as parking structures, are inefficient, prone to human error, and slow. Property managers and security teams require an automated solution to monitor vehicle entry and exit without causing traffic bottlenecks. Implementing an automated, high-speed license plate recognition system solves this by modernizing vehicle authentication and tracking infrastructure.

## Solution Overview
The application takes raw images of vehicles as input and automatically localizes the exact coordinates of the license plate. The system then crops this region of interest, applies dedicated contrast and resolution enhancements, and passes the optimized array to an optical character recognition (OCR) engine. The final output is the extracted text string of the license plate, which can be cross-referenced against a database for automated access control.

## Technical Approach
- **CV Technique:** Multi-component (Object Detection + Text Recognition)
- **Model Architecture:** A convolutional neural network (CNN)-based object detection model (YOLOv11) is used to locate license plates, while EasyOCR uses deep learning to recognize the text on the plates.*
- **Model:** YOLOv11 (Detection) and EasyOCR (Recognition)
- **How we will use it:** Transfer learning / Fine-tuning the pretrained YOLOv11 model on targeted license plate assets, combined with the open-source pretrained EasyOCR engine for out-of-the-box character mapping.
- **Framework:** PyTorch & OpenCV
- **Why this approach:** YOLOv11 provides state-of-the-art real-time detection speeds and structural accuracy, while EasyOCR’s deep learning backbone handles real-world text distortions much more effectively than traditional character segmentation frameworks like Tesseract.

## Dataset
- **Source:** Roboflow Universe
- **Size:** 10,000+ annotated vehicle and license plate images
- **Labels:** Bounding boxes for `license-plate` regions
- **Link:** [Roboflow License Plate Recognition Dataset](https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e)

## Success Metrics (what we will measure and expect)
- **🎯 Primary:** Mean Average Precision at a 0.5 Intersection over Union threshold ($mAP@0.5$) $\ge 90\%$. This measures how accurately the model localizes plates and how tightly the bounding boxes align with ground-truth coordinates.
- **⚡ Secondary:** Inference Latency $< 0.2$ seconds per image. This guarantees the model processes incoming frames quickly enough to prevent delay in real-world deployment scenarios.

### 🎯 Primary Success Metric: Model Performance (mAP@0.5)

The model was evaluated against a target Mean Average Precision (mAP@0.5) of **≥ 0.90**. The results below demonstrate that the YOLOv8 model exceeded this baseline across both the validation and unseen test data splits.

| Evaluation Metric | Target Threshold | Validation Split | Test Split | Status |
| :--- | :--- | :--- | :--- | :--- |
| **mAP@0.50** | ≥ 0.9000 | 0.9686 | 0.9695 | ✅ **PASSED** |
| **mAP@0.50-0.95** | - | 0.6913 | 0.6912 | - |
| **Precision** | - | 0.9825 | 0.9903 | - |
| **Recall** | - | 0.9473 | 0.9456 | - |

## Milestone Plan
| Phase | Task Description | Target Week | Status |
| :--- | :--- | :---: | :---: |
| **Phase 1: Blueprint** | Set up GitHub repository, secure compute environments (Colab/Kaggle/Heidi), and verify access to the Roboflow dataset. | Week 4 | 🟩 Complete |
| **Phase 2: First Working Demo** | Train a baseline YOLOv11 model on the dataset and write the basic pipeline code to crop detected plates. | Week 6 | 🟨 In Progress |
| **Phase 3: Make It Yours** | Integrate EasyOCR into the pipeline and add the custom OpenCV pre-processing filters to boost character legibility. | Week 8 | ⬜ Planned |
| **Phase 4: Improve and Measure** | Benchmark the primary $mAP@0.5$ and secondary inference latency metrics against the target success goals. | Week 10 | ⬜ Planned |
| **Phase 5: Build** | Test the end-to-end pipeline using out-of-distribution validation images collected directly from real parking structures. | Week 12 | ⬜ Planned |

## Resources
- **Compute:** Google Colab, Kaggle Notebooks, and Heidi Local/Institutional Cluster.
- **Cost:** $0 (Exclusively utilizing free GPU computing tiers and open-source models; optional $10 Colab Pro expansion if longer training sessions are required).

## Risks and Mitigation
| Risk | Probability | Plan B |
| :--- | :---: | :--- |
| **YOLOv11 struggles with extreme lighting or off-center angles** (resulting in missed plates). | **Low** | Proactively mitigated by selecting a highly diverse, 10k+ image Roboflow dataset. If drops occur, implement inference-time enhancements like **CLAHE** (to normalize shadows) and Test-Time Augmentation (**TTA**) to stabilize bounding boxes without needing to retrain the model. |
| **EasyOCR misreads the extracted text** due to low resolution, shadow gradients, or blurring in the cropped bounding boxes. | **High** | Implement a strict OpenCV pre-processing pipeline (**grayscale, cubic upscaling, and adaptive thresholding**) on the cropped image arrays before passing them to the OCR engine to maximize character edge contrast. |

## Demo Video
*[Link to project walkthrough video will be added during Final presentation submissions]*

## AI Usage Log
See [docs/AI_usage_log.md](docs/AI_usage_log.md)

## Current Status
- [x] Repository created
- [x] Proposal submitted
- [ ] First working demo
- [ ] System works on our data
- [ ] Metrics measured
- [ ] Final submitted
