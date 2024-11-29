import cv2
import easyocr
from ultralytics import YOLO

class LicensePlateDetector:
    def __init__(self, model, ocr_languages=["en"], ocr_confidence_threshold=0.5):
        self.model = model
        self.reader = easyocr.Reader(ocr_languages)
        self.confidence_threshold = ocr_confidence_threshold
        self.detected_plates = set() 

    def process_frame(self, frame):
        resized_img = self.resize_frame(frame)
        gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        results = self.model.predict(resized_img, verbose=False)
        if len(results[0].boxes.xyxy ) >= 1:
            num_objects = len(results[0].boxes.xyxy)
            for i in range(num_objects):
                x_min, y_min, x_max, y_max = map(int, results[0].boxes.xyxy[i])
                cv2.rectangle(resized_img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                cropped_img = gray_img[y_min:y_max, x_min:x_max]
                plate_text = self.perform_ocr(cropped_img)
                
                if plate_text:
                    self.detected_plates.add(plate_text)
                    cv2.putText(
                        resized_img,
                        plate_text,
                        (x_min, y_min - 10),
                        cv2.FONT_HERSHEY_PLAIN,
                        2,
                        (0, 255, 0),
                        2,
                    )

        return resized_img

    def resize_frame(self, frame, scale=0.33):
        return cv2.resize(frame, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)))

    def perform_ocr(self, cropped_img):
        ocr_results = self.reader.readtext(cropped_img)
        for (_, text, conf) in ocr_results:
            if conf > self.confidence_threshold:
                return text
        return ""

    def get_detected_plates(self):
        return list(self.detected_plates)


def process_video(video_path, detector, output_window_name="Detected License Plates"):
    cap = cv2.VideoCapture(video_path)

    while True:
        success, frame = cap.read()
        if not success:
            print("Кінець відео або помилка зчитування кадру.")
            break

        processed_frame = detector.process_frame(frame)

        cv2.imshow(output_window_name, processed_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():

    model = YOLO('best.pt')  # Завантажте вашу модель тут (замість ...)

    detector = LicensePlateDetector(model=model)

    video_path = "Car_traffic_live.mp4"  # Шлях до відео

    process_video(video_path, detector)

    print("Знайдені унікальні номери:", detector.get_detected_plates())

if __name__ == "__main__":
    main()
