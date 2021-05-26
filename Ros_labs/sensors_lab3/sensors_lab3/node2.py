#!/usr/bin/env python3


import rclpy
import serial

from rclpy.node import Node 
from nav_msgs.msg import Odometry
class my_node(Node):
    def __init__(self):
        super().__init__("node1")
        self.counter = 0
        self.create_timer(1/2,self.timer_call)
        self.obj_pub_num= self.create_publisher(Odometry,"Vel",rclpy.qos.qos_profile_sensor_data)
        self.get_logger().info("Node is started now")

    def timer_call(self):
        arduino = serial.Serial(port='/dev/ttyACM2', baudrate=9600, timeout=.1)
        value = arduino.readline()
        v1 = float(value.split(',')[0])
        v2 = float(value.split(',')[1])
        
        message = Odometry()
        message.twist.twist.angular.z = 0
        message.twist.twist.linear.x = (v1+v2)/2
      
        self.obj_pub_num.publish(message)


def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()
