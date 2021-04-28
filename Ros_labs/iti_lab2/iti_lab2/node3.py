#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from example_interfaces.srv import SetBool

class my_client(Node):
    def __init__(self):
        super().__init__("node3")
        self.service_client()


    def service_client(self):
        client=self.create_client((SetBool), "server")
        while client.wait_for_service(0.25) ==False:
            self.get_logger().warn("waiting for server")

        request = SetBool.Request()
        request.data = True
        future_obj = client.call_async(request)
        future_obj.add_done_callback(self.future_call)


    def future_call(self,future_msg):
        self.get_logger().info(str(future_msg.result().message))
       

def main(args = None):
    rclpy.init(args=None)
    node = my_client()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()
