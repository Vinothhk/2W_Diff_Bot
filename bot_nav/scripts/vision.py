#! /usr/bin/env python3

import rclpy
from rclpy.node import Node,QoSProfile
import cv2
from cv_bridge import CvBridge,CvBridgeError

from std_msgs.msg import String
from sensor_msgs.msg import Image

class CvNode(Node):
    def __init__(self):
        super().__init__('CVnode')
        self.rgbimage_pub = self.create_subscription(Image,"camera_depth/image_raw",self.rgb_callback,10)
        self.depthimage_pub = self.create_subscription(Image,"camera_depth/depth/image_raw",self.depth_callback,10)
        self.bridge = CvBridge()
        
    def rgb_callback(self,data):
        try:
            rgb_image = self.bridge.imgmsg_to_cv2(data,"bgr8")
        except CvBridgeError as e:
            print(e)
            
        (rows,cols,channels) = rgb_image.shape
        cv2.imshow('RGB image',rgb_image)
        cv2.waitKey(3)
    
    def depth_callback(self,data):
        try:
            depth_image = self.bridge.imgmsg_to_cv2(data,"32FC1")
        except CvBridgeError as e:
            print(e)
            
        #***(rows,cols,depth,channels) = depth_image.shape
        cv2.imshow('Depth image',depth_image)
        cv2.waitKey(3)
        
def main(args=None):
    rclpy.init(args=args)
    cvnode = CvNode()
    rclpy.spin(cvnode)
    cvnode.destroy_node()
    rclpy.shutdown()
    
if __name__ =='__main__' :  
    main()