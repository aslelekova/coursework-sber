from roboflow import Roboflow
from ultralytics import YOLO

rf = Roboflow(api_key="mSFbDvx11o3YDKGIdgsS")
project = rf.workspace("classification-glt8h").project("871sber")
version = project.version(1)
dataset = version.download("yolov11")

base_model_path = "/Users/anastasialelekova/PycharmProjects/sber/yolo11n.pt"
save_dir = "yolo_checkpoints"

epoch_stages = [75, 100]

last_checkpoint = "yolo_checkpoints/train_50/weights/best.pt"

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

