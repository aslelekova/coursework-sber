from ultralytics import YOLO

model = YOLO("/Users/anastasialelekova/PycharmProjects/pythonProject9/yolo_classification_checkpoints/train_50/weights/best.pt")
# model = YOLO("/Users/anastasialelekova/PycharmProjects/pythonProject9/runs/detect/train13/weights/best.pt")
test_data = "/Users/anastasialelekova/PycharmProjects/pythonProject9/cropped_atms"  # Путь к папке с тестовыми изображениями

results = model.predict(
    test_data,
    imgsz=640,
    device="cpu",
    save=True,
    project="results_folder",
    name="test_run"
)

print(f"Results saved to: {results[0].save_dir}")