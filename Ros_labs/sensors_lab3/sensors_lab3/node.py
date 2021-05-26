#!/usr/bin/env python3


import rclpy
import serial

from rclpy.node import Node 
#from nav_msgs.msg import Float

from std_msgs.msg import String

class my_node(Node):
    def __init__(self):
        super().__init__("node1")
        self.counter = 0
        self.create_timer(1/30,self.timer_call)
        self.obj_pub_num= self.create_publisher(String,"Vel",rclpy.qos.qos_profile_sensor_data)
        self.get_logger().info("Node is started now")

    def timer_call(self):
        arduino = serial.Serial(port='/dev/ttyACM2', baudrate=9600, timeout=.1)
        value = arduino.readline()
        
        message = String()
        message.data = value

        self.obj_pub_num.publish(message)


def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()
