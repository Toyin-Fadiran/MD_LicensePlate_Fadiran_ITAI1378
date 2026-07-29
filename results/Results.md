### 🎯 Primary Success Metric: Model Performance (mAP@0.5)

The model was evaluated against a target Mean Average Precision (mAP@0.5) of **≥ 0.90**. The results below demonstrate that the YOLOv8 model exceeded this baseline across both the validation and unseen test data splits.

| Evaluation Metric | Target Threshold | Validation Split | Test Split | Status |
| :--- | :--- | :--- | :--- | :--- |
| **mAP@0.50** | ≥ 0.9000 | 0.9686 | 0.9695 | ✅ **PASSED** |
| **mAP@0.50-0.95** | - | 0.6913 | 0.6912 | - |
| **Precision** | - | 0.9825 | 0.9903 | - |
| **Recall** | - | 0.9473 | 0.9456 | - |

### ⚡ Secondary Success Metric: Production Inference Latency

The system requires an inference latency of **< 0.2 seconds (200 ms)** per image to ensure real-time processing capabilities without bottlenecking the pipeline. The YOLOv8 spatial detection model comfortably exceeded this requirement during real-world batch processing.

| Execution Environment | Preprocess | Inference (Core) | Postprocess | Total Latency | Target (Inference) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Colab GPU (Production)** | 5.3 ms | **4.2 ms** | 1.8 ms | 11.3 ms | < 200.0 ms | ✅ **PASSED** |

*Note: An inference time of 4.2 milliseconds equates to 0.0042 seconds, meaning the production model operates ~47x faster than the required real-time baseline.*
