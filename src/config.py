from dataclasses import dataclass, field
from typing import List

@dataclass
class DetectorConfig:
    model_path: str = "yolov8n.pt"
    conf_threshold: float = 0.35
    iou_threshold: float = 0.45
    img_size: int = 640
    device: str = "cuda"
    classes_of_interest: List[int] = field(default_factory=lambda: [0, 2, 3, 5, 7])
    # 0=person,2=car,3=motorcycle,5=bus,7=truck
