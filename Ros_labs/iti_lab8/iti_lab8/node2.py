#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from example_interfaces.msg import String 



class my_node(Node):
    def __init__(self):
        super().__init__("node2")
        self.counter = 0
        self.pub_counter = 0
        self.create_subscription(String,"message",self.sub_call,10)
        self.get_logger().info("Subscriber  is started now")

    def sub_call(self,msg):
        self.get_logger().info(msg.data)



        
        








  
def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()