#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from turtlesim.msg import Pose



class my_node(Node):
    def __init__(self):
        super().__init__("node1")
        self.counter = 0
        #self.create_subscription(String,"/my_topic",self.sub_call,10)
        self.subscription = self.create_subscription(Pose, '/turtle1/custom_pose', self.sub_call, rclpy.qos.qos_profile_sensor_data)
        self.get_logger().info("Subscriber  is started now")

 

    def sub_call(self,msg):
        print(str(msg.x) + "  "+ str(msg.y))



  
def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()