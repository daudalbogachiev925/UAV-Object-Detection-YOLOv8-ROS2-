# UAV-Object-Detection-YOLOv8-ROS2-
 Детекция объектов с дрона в реальном времени, интеграция с ROS2, публикация bounding boxes + геолокация.
# UAV Object Detection
YOLOv8 + ROS2 — детекция объектов с дрона в реальном времени + геолокация.

## Возможности
- Real-time detection (YOLOv8n/s/m)
- ROS2 integration (vision_msgs)
- Пиксель → GPS координата
- Docker + NVIDIA GPU

## Запуск
```bash
pip install -r requirements.txt
python -m src.ros_node
```
