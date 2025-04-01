from ultralytics import YOLO
import os

# Путь к базовой модели (предобученной)
BASE_MODEL_PATH = "yolo11n.pt"

# Папка, в которую будут сохраняться модели
SAVE_DIR = "checkpoints/detection/yolo_detection_checkpoints"

# Этапы обучения по количеству эпох
EPOCH_STAGES = [10, 25, 50, 75, 100]

# YAML-файл с описанием датасета
DATA_YAML_PATH = "datasets/raw_detection_dataset/data.yaml"

def train_detection_model():
    """
    Многоэтапное обучение модели детекции YOLO.
    На каждой итерации модель дообучается с новым количеством эпох,
    а затем сохраняется чекпоинт и считается валидация.
    """
    last_checkpoint = BASE_MODEL_PATH

    for epochs in EPOCH_STAGES:
        print(f"\nОбучаем модель до {epochs} эпох...")

        model = YOLO(last_checkpoint)

        train_results = model.train(
            data=DATA_YAML_PATH,
            epochs=epochs,
            imgsz=640,
            device="cpu",
            save=True,
            project=SAVE_DIR,
            name=f"train_{epochs}"
        )

        last_checkpoint = os.path.join(SAVE_DIR, f"train_{epochs}", "weights", "best.pt")
        print(f"Модель сохранена в: {last_checkpoint}")

        metrics = model.val()
        print(f"Результаты валидации: {metrics.results_dict}")

    export_final_model(last_checkpoint)


def export_final_model(checkpoint_path):
    """
    Экспорт финальной модели в ONNX-формат.
    """
    print("\nЭкспортируем финальную модель в ONNX...")
    final_model = YOLO(checkpoint_path)
    path = final_model.export(format="onnx")
    print(f"Финальная модель экспортирована в: {path}")


if __name__ == "__main__":
    train_detection_model()
