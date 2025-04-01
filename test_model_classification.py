import os
from PIL import Image
from torchvision import transforms
from ultralytics import YOLO
import shutil

# Загружаем модель
model = YOLO("yolo_classification_checkpoints/train_100/weights/best.onnx", task="classify")

# Путь к изображениям, которые нужно распределить
input_folder = "/Users/anastasialelekova/Downloads/archive"

# Папка, куда будут разложены изображения
output_root = "/Users/anastasialelekova/Downloads/sorted"
os.makedirs(os.path.join(output_root, "clean"), exist_ok=True)
os.makedirs(os.path.join(output_root, "dirty"), exist_ok=True)

# Трансформация, как при обучении
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
])

# Проход по файлам
for filename in os.listdir(input_folder):
    img_path = os.path.join(input_folder, filename)
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    img = Image.open(img_path).convert("RGB")
    input_tensor = transform(img).unsqueeze(0)

    pred_class = model(input_tensor)[0].probs.top1
    pred_label = "clean" if pred_class == 0 else "dirty"

    dest_path = os.path.join(output_root, pred_label, filename)
    shutil.copy(img_path, dest_path)
    print(f"{filename} → {pred_label}")
