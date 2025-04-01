from roboflow import Roboflow
from ultralytics import YOLO

base_model_path = "/Users/anastasialelekova/PycharmProjects/sber/yolo11n.pt"
save_dir = "yolo_deyection_checkpoints"

epoch_stages = [10, 25, 50, 75, 100]

last_checkpoint = base_model_path

for epochs in epoch_stages:
    print(f"Обучаем модель до {epochs} эпох...")

    model = YOLO(last_checkpoint)

    train_results = model.train(
        data="/Users/anastasialelekova/PycharmProjects/sber/871sber-1/data.yaml",
        epochs=epochs,
        imgsz=640,
        device="cpu",
        save=True,
        project=save_dir,
        name=f"train_{epochs}"
    )

    last_checkpoint = f"{save_dir}/train_{epochs}/weights/best.pt"
    print(f"Модель сохранена в: {last_checkpoint}")

    metrics = model.val()

final_model = YOLO(last_checkpoint)
path = final_model.export(format="onnx")
print(f"Финальная модель экспортирована в: {path}")
