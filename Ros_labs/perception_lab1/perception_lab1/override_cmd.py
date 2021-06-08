#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from carkyo_msgs.msg import CameraEmergency
import numpy as np
class my_node(Node):
    def __init__(self):
        super().__init__("node1")
        self.min_dis = 0.0
        self.min_dis_cam = 0.0
        self.vel_x = 0.0
        self.vel_z = 0.0
        self.camera_emergency_stop = False
        self.create_timer(1/10,self.timer_call)
        self.obj_pub_num= self.create_publisher(Twist,"/cmd_vel",10)
        self.create_subscription(Twist,"/key_cmd_vel",self.sub_call,10)
        self.create_subscription(LaserScan,"/scan",self.lidar_reading,10)
        self.create_subscription(CameraEmergency,"/emergency",self.camera_emergency_reading,10)
        self.get_logger().info("Node is started now")
	
	
    def camera_emergency_reading(self, msg):
        self.camera_emergency_stop = msg.close_obstacle_detected
        self.min_dis_cam = msg.min_distance
        
    def lidar_reading(self, msg):
        detection_range = 20
        arr = msg.ranges[0:detection_range]+msg.ranges[-detection_range:]
        self.min_dis = min(arr)

    def sub_call(self, msg_in):
    

        self.vel_x = msg_in.linear.x
        self.vel_z = msg_in.angular.z

    def timer_call(self):
        message_out = Twist()


	
        if ((self.min_dis >0.6) and (self.min_dis_cam > 0.6)) and (self.vel_x > 0.0):
            message_out.linear.x = float(self.vel_x)
        else:
            message_out.linear.x = 0.0
        
        message_out.angular.z = float(self.vel_z)

        self.obj_pub_num.publish(message_out)

        self.get_logger().info(" min distance lidar = {},min distance cam = {},camera emergency = {}, velocity = {}".format(str(self.min_dis),self.min_dis_cam,self.camera_emergency_stop, str(self.vel_x)))


def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()
