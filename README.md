## Проект: Обнаружение загрязнённых банкоматов

Цель — обнаружить **загрязнения на банкоматах**, используя **YOLO**: сначала локализуем банкомат на изображении, потом классифицируем как `clean` или `dirty`.

## Архитектура

1. **Детекция банкоматов** (`models/yolo11n.pt`)
   - Обучение: `detection/train.py`
   - Кроп изображений: `data/crop_atms_for_classification.py`

2. **Классификация банкоматов** (`models/yolov8n-cls.pt`)
   - Обучение: `classification/train.py`

3. **FastAPI-сервер** (`api/main.py`)
   - Загружает изображение → детектирует банкомат → кропает → классифицирует

---

## Почему YOLO?

- **End-to-end**: работает без дополнительной обработки
- **Быстрая**: идеальна для реального времени
- **Точная**: подходит для маленьких объектов

---

## Roboflow

Платформа **[Roboflow](https://roboflow.com)** использовалась для:

- Разметки изображений банкоматов (bounding boxes).
- Аугментаций: повороты, размытие, контраст, шум.
- Экспорта в формат YOLO.
- Автоматического формирования `data.yaml`.

Импорт размеченных данных осуществляется с помощью скриптов:
- `data/import_dataset_detection.py`
- `data/import_dataset_classification.py`

---

## Датасеты

- `datasets/raw_classification_dataset/` — датасет для классификации (необрезанные фото) 
- `datasets/processed_classification_dataset/` — датасет для классификации (обрезанные фото)
- `datasets/raw_detection_dataset/` — размеченные изображения для детекции
- `datasets/detection_test/` — тесты детекции
- `datasets/classification_test/` — тесты классификации

---

## Запуск

### Установить зависимости
```bash
pip install -r requirements.txt
```

### Обучение моделей
```bash
python detection/train.py
python classification/train.py
```

### Запуск API
```bash
cd api
uvicorn main:app --reload --port 5500
```

---

## Модели

| Назначение     | Путь к модели |
|----------------|---------------|
| Детекция       | `models/yolo11n.pt` |
| Классификация  | `models/yolov8n-cls.pt` |

---

## Примеры изображений

[Смотреть на Яндекс.Диске](https://disk.yandex.ru/d/pqK9be7LM9J4lg)

