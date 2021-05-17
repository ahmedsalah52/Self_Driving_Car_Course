#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from example_interfaces.msg import String ,Int64
class my_node(Node):
    def __init__(self):
        super().__init__("node1")
        self.flag = True
        self.create_timer(1,self.timer_call)
        self.obj_pub_num= self.create_publisher(String,"message",10)
        self.get_logger().info("Node is started now")

    def timer_call(self):
    
        date_ = String()
        if  self.flag:
            date_.data = "Hello"
        else:
            date_.data = "Hi"
        self.flag = not self.flag

        self.obj_pub_num.publish(date_)


def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()