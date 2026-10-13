import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vision_msgs.msg import Detection2DArray, Detection2D, ObjectHypothesisWithPose
from cv_bridge import CvBridge
from src.detector import UAVDetector
from src.config import DetectorConfig

class DetectorNode(Node):
    def __init__(self):
        super().__init__("uav_detector")
        self.declare_parameter("model_path", "yolov8n.pt")
        self.detector = UAVDetector(DetectorConfig(
            model_path=self.get_parameter("model_path").value))
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, "/camera/image_raw", self.cb, 10)
        self.pub = self.create_publisher(Detection2DArray, "/detections", 10)
        self.get_logger().info("UAV Detector node started")

    def cb(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        dets = self.detector.infer(frame)
        arr = Detection2DArray()
        arr.header = msg.header
        for d in dets:
            det = Detection2D()
            x1, y1, x2, y2 = d["bbox"]
            det.bbox.center.position.x = (x1 + x2) / 2
            det.bbox.center.position.y = (y1 + y2) / 2
            det.bbox.size_x = x2 - x1
            det.bbox.size_y = y2 - y1
            hyp = ObjectHypothesisWithPose()
            hyp.hypothesis.class_id = d["class_name"]
            hyp.hypothesis.score = d["confidence"]
            det.results.append(hyp)
            arr.detections.append(det)
        self.pub.publish(arr)

def main():
    rclpy.init()
    node = DetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
