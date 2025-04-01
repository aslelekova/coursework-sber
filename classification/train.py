from ultralytics import YOLO
import torch


def main():
    """
    Обучает классификационную модель YOLO по стадиям (10, 25, 50, 75, 100 эпох),
    сохраняет чекпоинты и экспортирует финальную модель в формате ONNX.
    Также запускается финальная валидация.
    """

    # Пути к данным и модели
    dataset_path = "datasets/cropped_classification_dataset"
    initial_weights = "models/yolov8s-cls.pt"
    save_dir = "../checkpoints/classification/yolo_classification_checkpoints"

    # Этапы обучения по эпохам
    epoch_stages = [10, 25, 50, 75, 100]
    last_checkpoint = initial_weights

    # Обучение по этапам
    for epochs in epoch_stages:
        print(f"Обучаем классификационную модель до {epochs} эпох...")

        model = YOLO(last_checkpoint)
        train_results = model.train(
            data=dataset_path,
            imgsz=224,
            device="cuda" if torch.cuda.is_available() else "cpu",
            save=True,
            project=save_dir,
            name=f"train_{epochs}",
            epochs=epochs
        )

        last_checkpoint = f"{save_dir}/train_{epochs}/weights/best.pt"
        print(f"Модель после {epochs} эпох сохранена в: {last_checkpoint}")

    # Экспорт финальной модели в ONNX
    final_model = YOLO(last_checkpoint)
    onnx_path = final_model.export(format="onnx")
    print(f"Финальная модель экспортирована в: {onnx_path}")

    # Валидация финальной модели
    test_results = final_model.val(
        data=dataset_path,
        split='test',
        imgsz=224,
        device="cuda" if torch.cuda.is_available() else "cpu"
    )

    print("Результаты валидации:")
    print(test_results)


if __name__ == "__main__":
    main()
