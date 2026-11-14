# ATM Cleanliness Inspection

A computer vision coursework project for screening ATM photos for visible dirt. The system locates each ATM in a scene and returns its bounding box, a `clean` or `dirty` label, and a classification confidence score.

## How it works

1. **Detect ATMs.** A YOLO11n detector processes the full photograph. The API uses a detection confidence threshold of 0.50.
2. **Classify each ATM.** The API crops each detected region, resizes it to 224 × 224 pixels, and passes it to a YOLOv8n classifier. The label describes the entire ATM crop.

The [FastAPI backend](api/main.py) exposes this pipeline through `POST /detect`, which accepts a multipart file field named `upload_image`. The [Flutter client](atm_machine__app/lib/) lets users take a photo or select one from the gallery and displays the coordinates, label, and confidence for each detected ATM.

## Data and training

The project used Roboflow to prepare two datasets. The detection export contains ATM bounding boxes in YOLO format. The classification export groups full photos by cleanliness label. The [crop script](data/crop_atms_for_classification.py) runs the trained detector on these photos and saves the resulting crops under the original labels and train, validation, and test splits.

The training scripts use a 640-pixel input size for detection and a 224-pixel input size for classification. Each subsequent fine-tuning stage starts from the previous stage's best checkpoint, and the scripts export the final models to ONNX. Retraining requires the corresponding Roboflow exports.

## Validation results

| Model | Validation metric recorded in the checkpoint | Checkpoint used by the API |
| --- | --- | --- |
| YOLO11n detector | **99.34%** mAP@0.50, **92.23%** mAP@0.50:0.95 | [`train13/weights/best.pt`](checkpoints/detection/yolo_detection_checkpoints/detect/train13/weights/best.pt) |
| YOLOv8n classifier | **92.98%** top-1 accuracy on ATM crops | [`train_100/weights/best.pt`](checkpoints/classification/yolo_classification_checkpoints/train_100/weights/best.pt) |

These figures describe validation of the two models on their respective tasks.

## Repository guide

| Path | Contents |
| --- | --- |
| [`data/`](data/) | Roboflow import scripts and ATM crop generation |
| [`detection/train.py`](detection/train.py) and [`classification/train.py`](classification/train.py) | Fine-tuning scripts |
| [`models/`](models/) and [`checkpoints/`](checkpoints/) | Base weights, trained checkpoints, and [classifier training logs](checkpoints/classification/yolo_classification_checkpoints/) |
| [`api/`](api/) and [`atm_machine__app/`](atm_machine__app/) | Inference API and Flutter client |

## Run inference locally

```bash
git clone --depth 1 https://github.com/aslelekova/coursework-sber.git
cd coursework-sber
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install "torch==2.6.0" "torchvision==0.21.0" "ultralytics==8.3.76" \
  fastapi uvicorn aiofiles loguru python-multipart
```

In [`api/main.py`](api/main.py), replace the hard-coded paths in the `detector` and `classifier` initializers with the paths to their respective checkpoints in the table above. From the repository root, start the API.

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

In another terminal, submit a photo using its local file path.

```bash
curl --fail-with-body -F 'upload_image=@/path/to/atm.jpg' http://127.0.0.1:8000/detect
```
