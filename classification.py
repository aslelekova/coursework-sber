from ultralytics import YOLO
import torch

classification_model_path = "/Users/anastasialelekova/PycharmProjects/pythonProject9/yolo11n-cls.pt"  # Путь к модели классификации

classification_model = YOLO("yolo11n-cls.yaml").load(classification_model_path)
epoch_stages = [10, 25, 50]
save_dir = "yolo_classification_checkpoints"
last_checkpoint = classification_model_path

for epochs in epoch_stages:
    print(f"Обучаем классификационную модель до {epochs} эпох...")
    classification_model = YOLO(last_checkpoint)
    train_results = classification_model.train(
        data="/Users/anastasialelekova/PycharmProjects/pythonProject9/processed_dataset",
        imgsz=64,
        device="cuda" if torch.cuda.is_available() else "cpu",
        save=True,
        project=save_dir,
        name=f"train_{epochs}"
    )
    last_checkpoint = f"{save_dir}/train_{epochs}/weights/best.pt"
    print(f"Модель сохранена в: {last_checkpoint}")

final_model = YOLO(last_checkpoint)
path = final_model.export(format="onnx")
print(f"Финальная модель классификации экспортирована в: {path}")
