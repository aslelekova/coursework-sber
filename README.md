

## Описание проекта
Цель проекта — **обнаружение загрязнений на экранах банкоматов** с помощью компьютерного зрения.

Архитектура:
- **YOLOv11 detection** — находит экран банкомата
- **YOLOv11 classification** — определяет состояние экрана (clean / dirty)

---

## Структура проекта
```
├── API_Docs-master/                    # Документация API
├── runs/detect/                       # Результаты детекции
├── yolo_classification_checkpoints/   # Чекпоинты классификации
│
├── classification.py                  # Классификация clean / dirty
├── detect_atm_and_crop.py             # Детекция банкомата и кроп экрана
├── detection.py                       # YOLO-детекция
├── import_dataset.py                  # Импорт общего датасета
├── import_dataset_classification.py   # Импорт датасета для классификации
├── import_dataset_detection.py        # Импорт датасета для детекции
├── main.py                            # Основной пайплайн
├── split_dirty_clean.py               # Сплитинг датасета на clean / dirty
├── test_model.py                      # Тестирование классификатора
│
├── yolo11n.pt                         # Веса YOLO модели детекции
├── yolo11n-cls.pt                     # Веса YOLO классификатора
└── README.md                          # Этот файл
```

---

## Описание датасета
В проекте используется **пользовательский датасет банкоматов**, размеченный на 2 класса:
```
dataset/
├── clean/    # Чистые экраны
├── dirty/    # Загрязнённые экраны
```
Импорт и разметка — скрипты:
- `import_dataset.py`
- `import_dataset_classification.py`
- `split_dirty_clean.py`

---

## Как запустить
### 1. Установка зависимостей
```bash
pip install torch torchvision ultralytics opencv-python matplotlib tqdm scikit-learn
```

### 2. Детекция 
```bash
python detection.py
```

### 3. Классификация 
```bash
python classification.py
```

### 4. Тестирование модели классификации
```bash
python test_model.py
```

---

## Используемые модели
- **yolo11n.pt** — модель детекции банкомата
- **yolo11n-cls.pt** — модель классификации состояния экрана
