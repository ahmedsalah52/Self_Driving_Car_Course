#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from std_srvs.srv import Empty
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import csv


class my_client(Node):
    def __init__(self):
        super().__init__("node")
        self.turtle_pos = [0.0,0.0,0.0] 
        self.moves_L_X = []
        self.moves_A_Z = []
        self.counter = 0
        self.create_subscription(Pose,"/turtle1/pose",self.sub_call_1,10) #to get the position of turtle_1 from topic /turtle1/pose
        self.turtle_1= self.create_publisher(Twist,"/turtle1/cmd_vel",10) # to publish the velocity to turtle_1 thats how we control turtle 1

        self.create_timer(1,self.timer_call)
        with open('/home/ahmed/ITI_ROS_WS/src/iti_lab_9/iti_lab_9/turtle_commands.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.moves_L_X.append(float(row['linear x']))
                self.moves_A_Z.append(float(row['angular z']))
        if len(self.moves_L_X) != len(self.moves_A_Z):
            self.get_logger().warn("linear and angular inputs are not with the same length")
        
    def timer_call(self):
        
        #load file /home/ahmed/ITI_ROS_WS/src/iti_lab_9/iti_lab_9/turtle_commands.csv

        
        

        velocity = Twist()
        velocity.linear.x = self.moves_L_X[self.counter]
        velocity.angular.z = self.moves_A_Z[self.counter]
        self.turtle_1.publish(velocity)

        self.counter += 1

        if self.counter == len(self.moves_L_X):
            self.counter = 0

        if (self.turtle_pos[0]>8) or (self.turtle_pos[0]<2) or (self.turtle_pos[1]>8) or (self.turtle_pos[1]<2) :
            self.Reset()


    def Reset(self):
        client=self.create_client(Empty, "reset")
        while client.wait_for_service(0.25) ==False:
            self.get_logger().warn("waiting for server")

        request = Empty.Request()
        future_obj = client.call_async(request)
        future_obj.add_done_callback(self.future_call)


    def future_call(self,future_msg):
        self.get_logger().info("Reset Done")


    def sub_call_1(self,msg):
        self.turtle_pos[0] = msg.x
        self.turtle_pos[1] = msg.y
        self.turtle_pos[2] = msg.theta


def main(args = None):
    rclpy.init(args=None)
    node = my_client()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()