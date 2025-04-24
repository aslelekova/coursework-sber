# Classifier validation

## 22 April 2025 — Metrics and ONNX review

Alexandra Ovsyannikova reviewed the classifier's validation metrics and checked
the ONNX export. The saved training log for the selected run reports a peak
validation top-1 accuracy of 92.98%.

- [Training log](../checkpoints/classification/yolo_classification_checkpoints/train_100/results.csv)
- [ONNX checkpoint](../checkpoints/classification/yolo_classification_checkpoints/train_100/weights/best.onnx)

## 24 April 2025 — Application test

Anastasiia Lelekova and Alexandra Ovsyannikova tested the classifier through
the FastAPI backend and the Flutter client.

- [FastAPI endpoint](../api/main.py)
- [Flutter client](../atm_machine__app/lib/main.dart)
