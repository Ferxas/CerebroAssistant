# vision/yolov_detector.py

from ultralytics import YOLO
import cv2
import time

class YOLOvDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(0)
        self.last_seen = []

    def analyze_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        results = self.model(frame)
        labels = []
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = r.names[cls]
                labels.append(label)
                cv2.putText(frame, label, (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        self.last_seen = labels
        return frame

    def run(self):
        print("Iniciando visión...")
        while True:
            frame = self.analyze_frame()
            if frame is not None:
                cv2.imshow("CEREBRO - Visión", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def get_last_seen(self):
        return list(set(self.last_seen))