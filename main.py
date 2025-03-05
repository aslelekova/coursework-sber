from roboflow import Roboflow
from ultralytics import YOLO

# Загрузка датасета
rf = Roboflow(api_key="mSFbDvx11o3YDKGIdgsS")
project = rf.workspace("classification-glt8h").project("871sber")
version = project.version(1)
dataset = version.download("yolov11")

# Пути к файлам модели

base_model_path = "/Users/anastasialelekova/PycharmProjects/sber/yolo11n.pt" # Начальная модель
save_dir = "yolo_checkpoints"  # Каталог для сохранения чекпойнтов

# Список эпох, на которых нужно остановиться
epoch_stages = [10, 25, 50, 75, 100]

# Переменная для хранения пути к последнему чекпойнту
last_checkpoint = base_model_path

# Поэтапное обучение
for epochs in epoch_stages:
    print(f"Обучаем модель до {epochs} эпох...")

    # Загружаем предыдущую модель (чтобы продолжить обучение)
    model = YOLO(last_checkpoint)

    # Запускаем обучение
    train_results = model.train(
        data="/Users/anastasialelekova/PycharmProjects/sber/871sber-1/data.yaml",  # YAML-файл датасета
        epochs=epochs,  # Обучаем до нужного числа эпох
        imgsz=640,  # Размер изображений
        device="cpu",  # Можно сменить на "cuda" при наличии GPU
        save=True,  # Сохраняем чекпойнты
        project=save_dir,  # Каталог сохранения
        name=f"train_{epochs}"  # Название эксперимента
    )

    # Путь к последнему чекпойнту модели
    last_checkpoint = f"{save_dir}/train_{epochs}/weights/best.pt"
    print(f"Модель сохранена в: {last_checkpoint}")

    # Оценка модели
    metrics = model.val()

# Финальный экспорт в ONNX
final_model = YOLO(last_checkpoint)
path = final_model.export(format="onnx")
print(f"Финальная модель экспортирована в: {path}")
