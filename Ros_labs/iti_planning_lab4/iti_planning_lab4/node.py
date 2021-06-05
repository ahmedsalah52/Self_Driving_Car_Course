#!/usr/bin/env python3
import rclpy

from rclpy.node import Node 
from nav_msgs.msg import Path
from functions import menger_curvature 
class my_node(Node):
    def __init__(self):
        super().__init__("sub_node")
        self.create_subscription(Path,"/local_plan",self.sub_call,10)
        self.get_logger().info("Subscriber is started now")

    def sub_call(self,msg):
        self.poses = msg.poses   #Path.poses[].pose.positions.x
        path_length = len(self.poses)
        if path_length <1:
            return 0
        start = self.poses[0].pose.position
        mid = self.poses[int((path_length)/2)].pose.position
        end = self.poses[-1].pose.position
        curve = menger_curvature(start.x,start.y,mid.x,mid.y,end.x,end.y)

        d = (mid.x - start.x) * (end.y - start.y) - (mid.y-start.y) * (end.x - start.x)
        
        if abs(curve) > 0.2:
            if d < 0:
                self.get_logger().info("The robot is turning right with a curvature {}".format(curve))
            else:
                self.get_logger().info("The robot is turning left with a curvature {}".format(curve))

        else:
            self.get_logger().info("The robot is moving straight")








  
def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()