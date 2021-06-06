#!/usr/bin/env python3
'''
- Create ROS Image Subscriber.
- Get image using CV-Bridge.
- Apply Shi-Tomasi corner detection on the image.
- Draw output points on a black image.
- Show both original and corners output image.
'''

import rclpy

from rclpy.node import Node 
from example_interfaces.msg import String ,Int64

from example_interfaces.srv import SetBool
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class my_node(Node):
    def __init__(self):
        super().__init__("node")
        self.image = np.zeros([240, 320, 3])
        self.create_subscription(Image,"/intel_realsense_d435_depth/image_raw",self.sub_call,rclpy.qos.qos_profile_sensor_data)
        self.get_logger().info("Subscriber  is started now")
        

    
    #def show(self):
        #gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        #corners = cv.goodFeaturesToTrack(gray,25,0.01,10)
        #corners = np.int0(corners)
        #for i in corners:
        #    x,y = i.ravel()
        #    cv.circle(img,(x,y),3,255,-1)
            

    def sub_call(self,msg):
        self.bridge = CvBridge()
        black = np.zeros([240, 320, 3])
        self.image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        gray = cv.cvtColor(self.image,cv.COLOR_BGR2GRAY)
        corners = cv.goodFeaturesToTrack(gray,25,0.01,10)
        corners = np.int0(corners)
        for i in corners:
            x,y = i.ravel()
            cv.circle(black,(x,y),3,255,-1)
        cv.imshow('current',self.image)
        cv.imshow('corners',black)

        cv.waitKey(0)
        cv.destroyAllWindows()       







  
def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)

    rclpy.shutdown()



if __name__ == "__main__":
    main()