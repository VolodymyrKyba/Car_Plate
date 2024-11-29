from ultralytics import YOLO

#Завантаження базової моделі
model = YOLO('yolov8n.pt')

# Навчання
model.train(data='config.yaml', epochs=50, imgsz=640)
