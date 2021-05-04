#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from msgs.msg import StringInt , Accumulator

from msgs.srv import FlagString


class my_node(Node):
    def __init__(self):
        super().__init__("node2")
        self.counter = 0
        self.pub_counter = 0
        self.create_subscription(StringInt,"number",self.sub_call,10)
        self.get_logger().info("Subscriber and server is started now")
        self.create_service(FlagString, 'server', self.srv_call)

        self.obj_pub_num= self.create_publisher(Accumulator,"counter",10)
    
    def srv_call(self,rq,rsp):
        if rq.flag == True:
            self.counter = 0
            self.pub_counter = Accumulator()
            self.pub_counter.number = 0
            self.obj_pub_num.publish(self.pub_counter)

            #rsp.message = "reset"
        self.get_logger().info(str(rq.flag))
        return rsp

    def sub_call(self,msg1):
        self.counter += msg1.number
        self.get_logger().info(msg1.message+str(self.counter))

        self.pub_counter = Accumulator()
        self.pub_counter.number = self.counter
        self.obj_pub_num.publish(self.pub_counter)


        
        








  
def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()