#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from msgs.msg import StringInt
class my_node(Node):
    def __init__(self):
        super().__init__("node1")
        self.counter = 0
        self.create_timer(1/2,self.timer_call)
        self.obj_pub_num= self.create_publisher(StringInt,"number",10)
        self.get_logger().info("Node is started now")

    def timer_call(self):
    
        message = StringInt()
        message.message = "Salah is publishing : "
        message.number = 5
        self.obj_pub_num.publish(message)


def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()