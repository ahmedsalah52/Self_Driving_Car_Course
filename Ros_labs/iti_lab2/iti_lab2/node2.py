#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from example_interfaces.msg import String ,Int64

from example_interfaces.srv import SetBool


class my_node(Node):
    def __init__(self):
        super().__init__("node2")
        self.counter = 0
        self.pub_counter = 0
        self.create_subscription(Int64,"number",self.sub_call,10)
        self.get_logger().info("Subscriber and server is started now")
        self.create_service(SetBool, 'server', self.srv_call)

        self.obj_pub_num= self.create_publisher(Int64,"counter",10)
    
    def srv_call(self,rq,rsp):
        if rq.data == True:
            self.counter = 0
            self.pub_counter = Int64()
            self.pub_counter.data = 0
            self.obj_pub_num.publish(self.pub_counter)

            rsp.message = "reset"
        self.get_logger().info(str(rq.data))
        return rsp

    def sub_call(self,msg1):
        self.counter += msg1.data
        self.get_logger().info(str(self.counter))

        self.pub_counter = Int64()
        self.pub_counter.data = self.counter
        self.obj_pub_num.publish(self.pub_counter)


        
        








  
def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()