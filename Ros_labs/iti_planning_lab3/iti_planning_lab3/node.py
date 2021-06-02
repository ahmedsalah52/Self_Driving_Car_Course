#!/usr/bin/env python3
import rclpy

from rclpy.node import Node 
from nav_msgs.msg import Path
from functions import menger_curvature 
class my_node(Node):
    def __init__(self):
        super().__init__("sub_node")
        self.create_subscription(Path,"/plan",self.sub_call,10)
        self.get_logger().info("Subscriber is started now")

    def sub_call(self,msg):
        self.poses = msg.poses   #Path.poses[].pose.positions.x
        path_length = len(self.poses)
        short_path = self.poses[0:int(path_length/5)]
        start = short_path[0].pose.position
        mid = short_path[int(len(short_path)/2)].pose.position
        end = short_path[-1].pose.position
        curve = menger_curvature(start.x,start.x,mid.x,mid.y,end.x,end.y)
        if abs(curve) <2:
            self.get_logger().info("The robot is turning with a curvature {}".format(curve))
        else:
            self.get_logger().info("The robot is moving straight")








  
def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()