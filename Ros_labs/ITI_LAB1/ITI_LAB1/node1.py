#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from example_interfaces.msg import String ,Int64
class my_node(Node):
    def __init__(self):
        super().__init__("node1")
        self.counter = 0
        self.create_timer(1/2,self.timer_call)
        self.obj_pub_num= self.create_publisher(String,"string",10)
        
        self.get_logger().info("Node is started now")
        self.create_subscription(String,"flag",self.sub_call,10)

    def timer_call(self):
    
        number = String()
        number.data = "Ahmed is publishing : " + str(self.counter)
        self.obj_pub_num.publish(number)
        self.counter +=1

    def sub_call(self,msg2):
        if msg2.data == 'True':
            self.counter = 0


def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()