import os
from pathlib import Path
from ultralytics import YOLO
from PIL import Image

model = YOLO("/yolo_detection_checkpoints/detect/train13/weights/best.pt")

input_dir = Path("/Users/anastasialelekova/Downloads/archive-3")
output_dir = Path("/Users/anastasialelekova/Downloads/cropped_atms")
output_dir.mkdir(parents=True, exist_ok=True)

image_extensions = [".jpg", ".jpeg", ".png"]
image_paths = [p for p in input_dir.rglob("*") if p.suffix.lower() in image_extensions]

for image_path in image_paths:
    results = model(image_path)

    for i, result in enumerate(results):
        im = Image.open(image_path).convert("RGB")

        for j, box in enumerate(result.boxes.xyxy):
            x1, y1, x2, y2 = map(int, box.tolist())
            cropped = im.crop((x1, y1, x2, y2))

            out_path = output_dir / f"{image_path.stem}_det{j}.jpg"
            cropped.save(out_path)

print(f"Обрезанные банкоматы сохранены в: {output_dir}")
