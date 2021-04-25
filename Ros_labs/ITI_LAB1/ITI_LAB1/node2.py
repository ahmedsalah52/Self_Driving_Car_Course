#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from example_interfaces.msg import String ,Int64
class my_node(Node):
    def __init__(self):
        super().__init__("node2")
        self.counter = 0
        self.flag = "False"

        self.create_subscription(String,"string",self.sub_call,10)
        self.get_logger().info("Subscriber is started now")
        self.obj_pub = self.create_publisher(String,"flag",10)
        self.obj_pub_counter = self.create_publisher(String,"counter",10)

    
   

    def sub_call(self,msg1):
        self.counter = msg1.data.split()[-1]
        self.get_logger().info(self.counter)

        if int(self.counter) == 5:
            self.get_logger().info('reset')
            self.flag = "True"
        else:
            self.flag = "False"
        

        msg2 = String()  
        msg2.data = self.flag 
        self.obj_pub.publish(msg2)

        counter = String()  
        counter.data = str(self.counter)
        self.obj_pub_counter.publish(counter)








  
def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()