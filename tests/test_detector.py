import numpy as np
from src.detector import UAVDetector
from src.config import DetectorConfig

def test_infer_returns_list():
    det = UAVDetector(DetectorConfig(model_path="yolov8n.pt", device="cpu"))
    frame = np.zeros((640, 640, 3), dtype=np.uint8)
    out = det.infer(frame)
    assert isinstance(out, list)
