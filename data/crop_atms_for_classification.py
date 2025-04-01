import os
import cv2
import shutil
from ultralytics import YOLO

# === Конфигурация ===
DETECTION_MODEL_PATH = "checkpoints/detection/yolo_detection_checkpoints/detect/train13/weights/best.pt"
INPUT_DATASET_PATH = "datasets/raw_classification_dataset"
OUTPUT_DATASET_PATH = "datasets/cropped_classification_dataset"
CONFIDENCE_THRESHOLD = 0.25

# Загрузка модели детекции
detection_model = YOLO(DETECTION_MODEL_PATH)


def detect_atm_and_crop(image_path: str, save_path: str):
    """
    Детектирует банкоматы на изображении и сохраняет вырезанные фрагменты.
    :param image_path: Путь к изображению
    :param save_path: Папка для сохранения вырезанных банкоматов
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Не удалось загрузить: {image_path}")
        return

    results = detection_model.predict(source=img, conf=CONFIDENCE_THRESHOLD, verbose=False)

    for i, box in enumerate(results[0].boxes.xyxy.cpu().numpy()):
        x1, y1, x2, y2 = map(int, box[:4])
        cropped_img = img[y1:y2, x1:x2]

        os.makedirs(save_path, exist_ok=True)
        filename = os.path.splitext(os.path.basename(image_path))[0]
        save_filename = os.path.join(save_path, f"{filename}_{i}.jpg")
        cv2.imwrite(save_filename, cropped_img)


def prepare_and_process_dataset():
    """
    Удаляет старую обработанную директорию, создаёт структуру,
    проходит по всем изображениям и применяет функцию детекции.
    """

    # Удаляем старую директорию
    if os.path.exists(OUTPUT_DATASET_PATH):
        shutil.rmtree(OUTPUT_DATASET_PATH)

    # Создаём структуру директорий
    for split in ["train", "valid", "test"]:
        for cls in ["clean", "dirty"]:
            os.makedirs(os.path.join(OUTPUT_DATASET_PATH, split, cls), exist_ok=True)

    # Обработка изображений
    for split in ["train", "valid", "test"]:
        for cls in ["clean", "dirty"]:
            input_folder = os.path.join(INPUT_DATASET_PATH, split, cls)
            output_folder = os.path.join(OUTPUT_DATASET_PATH, split, cls)

            for img_file in os.listdir(input_folder):
                if not img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                img_path = os.path.join(input_folder, img_file)
                detect_atm_and_crop(img_path, output_folder)

    print("\nОбработка завершена, все банкоматы вырезаны и сохранены")


if __name__ == "__main__":
    prepare_and_process_dataset()
