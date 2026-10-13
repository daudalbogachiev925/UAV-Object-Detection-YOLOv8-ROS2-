import numpy as np
from ultralytics import YOLO
from dataclasses import asdict
from src.config import DetectorConfig

class UAVDetector:
    def __init__(self, cfg: DetectorConfig):
        self.cfg = cfg
        self.model = YOLO(cfg.model_path)

    def infer(self, frame: np.ndarray):
        results = self.model.predict(
            frame, imgsz=self.cfg.img_size, conf=self.cfg.conf_threshold,
            iou=self.cfg.iou_threshold, device=self.cfg.device, verbose=False,
        )[0]
        detections = []
        for box in results.boxes:
            cls = int(box.cls[0])
            if cls not in self.cfg.classes_of_interest:
                continue
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append({
                "class_id": cls,
                "class_name": self.model.names[cls],
                "confidence": float(box.conf[0]),
                "bbox": [x1, y1, x2, y2],
                "center": [(x1 + x2) / 2, (y1 + y2) / 2],
            })
        return detections
