from ultralytics import YOLO
from utils import draw_defect

class DefectDetector:
    def __init__(self, model_path="yolov8n.pt", confidence=0.3):
        """
        Initialise the defect detector.
        Uses YOLOv8 as the base detection model.
        confidence: lower threshold to catch subtle defects
        """
        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, image):
        """
        Run defect detection on an image.
        Returns annotated image and structured defect data.
        """
        annotated = image.copy()
        defects = []

        results = self.model(image, conf=self.confidence)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                label = result.names[class_id]

                annotated = draw_defect(
                    annotated, x1, y1, x2, y2, label, confidence
                )

                width = x2 - x1
                height = y2 - y1
                area = width * height

                defects.append({
                    "type": label,
                    "confidence": round(confidence, 3),
                    "bbox": [x1, y1, x2, y2],
                    "area_px": area,
                    "severity": self._classify_severity(confidence, area)
                })

        return annotated, defects

    def _classify_severity(self, confidence, area):
        """Classify defect severity based on confidence and area."""
        if confidence > 0.8 or area > 10000:
            return "HIGH"
        elif confidence > 0.5 or area > 5000:
            return "MEDIUM"
        else:
            return "LOW"