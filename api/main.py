import os
import uuid
import shutil
import aiofiles
import uvicorn

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from ultralytics import YOLO
from PIL import Image
from pathlib import Path
from loguru import logger

# Загрузка моделей классификации и детекции
classifier = YOLO('/Users/anastasialelekova/PycharmProjects/pythonProject9/checkpoints/classification/yolo_classification_checkpoints/train_100/weights/best.pt')
detector = YOLO('/Users/anastasialelekova/PycharmProjects/pythonProject9/checkpoints/detection/yolo_detection_checkpoints/detect/train13/weights/best.pt')

# Создание временной директории для хранения изображений
tmp_dir = os.path.join(os.getcwd(), "api", "tmp")
if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)
os.makedirs(tmp_dir)

# Инициализация FastAPI-приложения
app = FastAPI()

# Настройка логгера: запись в файл debug.log с ротацией по размеру
logger.remove()
logger.add('debug.log', format="{time} {message}", level="DEBUG", rotation="2 MB", compression="zip")

# Разрешение CORS для всех источников (можно ограничить при необходимости)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@logger.catch
@app.post('/detect')
async def detect(upload_image: UploadFile):
    """
    Обработка загруженного изображения:
    1. Сохраняет изображение во временную директорию.
    2. Детектирует банкоматы на изображении.
    3. Вырезает каждый банкомат, классифицирует как "чистый" или "грязный".

    :param upload_image: Файл изображения (jpg/png)
    :return: JSON со списком найденных банкоматов, координатами и результатами классификации
    """
    try:
        # Сохраняем файл во временную папку
        filename = uuid.uuid4().hex + ".jpg"
        image_path = (Path(tmp_dir) / filename).absolute()
        async with aiofiles.open(image_path, 'wb') as image_file:
            await image_file.write(await upload_image.read())

        # Детектируем банкоматы
        detect_result = detector.predict(image_path, conf=0.5)[0]
        boxes = detect_result.boxes

        if boxes is None or len(boxes) == 0:
            return {"message": "No ATMs detected"}

        # Загружаем изображение и подготавливаем список результатов
        image = Image.open(image_path)
        results = []

        for box in boxes:
            # Получаем координаты и вырезаем банкомат
            coords = box.xyxy.tolist()[0]
            cropped = image.crop(coords).resize((224, 224))

            # Сохраняем вырезанный банкомат и классифицируем
            temp_path = os.path.join(tmp_dir, f"atm_crop_{uuid.uuid4().hex}.jpg")
            cropped.save(temp_path)

            classify_result = classifier.predict(temp_path)[0]
            label = classify_result.names[classify_result.probs.top1]
            conf = classify_result.probs.top1conf.item()

            results.append({
                "box": {"x1": coords[0], "y1": coords[1], "x2": coords[2], "y2": coords[3]},
                "classification": label,
                "confidence": round(conf, 4)
            })

        return JSONResponse({"detections": results})

    except Exception as e:
        logger.error(f"Exception: {e}")
        raise HTTPException(status_code=500, detail='Internal error')


# Запуск приложения
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5500, reload=True)


# if __name__ == '__main__':
#     uvicorn.run("main:app",
#                 host="83.166.239.26",
#                 port=5500,
#                 reload=True
#                 )