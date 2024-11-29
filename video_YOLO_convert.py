from ultralytics import YOLO
path_to_video = ""
path_to_model = ""
model = YOLO(path_to_model)
model.predict(path_to_video,save = True)