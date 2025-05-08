from ultralytics import YOLO
import cv2

class YOLOvDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def run_once(self):
        cap = cv2.VideoCapture(0)
        print("📷 Cámara activada.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model(frame)
            labels = []
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    label = r.names[cls]
                    labels.append(label)
                    cv2.putText(frame, label, (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            cv2.imshow("👁️ CEREBRO observando", frame)

            # Presiona 'q' para cerrar ventana de visión
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
