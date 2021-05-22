#!/usr/bin/env python3


import rclpy
from rclpy.node import Node 
from nav_msgs.msg import Odometry
import numpy as np
import csv


class my_node(Node):
    def __init__(self):
        super().__init__("node")
        self.x = []
        self.y = []
        self.yaw = []
        self.counter = 0
        self.check_points = [0,0,0,0]

        self.create_subscription(Odometry,"/odom",self.sub_call,rclpy.qos.qos_profile_sensor_data) 
        self.get_logger().info("Subscriber is started now")
        with open('pose.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.x.append(float(list(row.values())[0]))
                self.y.append(float(list(row.values())[1]))
                self.yaw.append(float(list(row.values())[2]))
        
    def sub_call(self,msg):
        #yaw_ = (msg.twist.twist.angular.z / 3.14) * 180
        r_x = msg.pose.pose.position.x
        r_y = msg.pose.pose.position.y
        
        roll, pitch, yaw_ = self.euler_from_quaternion(msg.pose.pose.orientation)
        yaw_ = (yaw_ / 3.14) * 180
        self.get_logger().info(str(self.x[self.counter]) + " x "+str(r_x)) #msg.twist.twist.linear.x
        self.get_logger().info(str(self.y[self.counter]) + " y "+str(r_y))
        self.get_logger().info(str(self.yaw[self.counter]) + " yaw "+str(yaw_))
        self.get_logger().info(str(self.check_points[0]) + " "+str(self.check_points[1]) + " "+str(self.check_points[2]) + " "+str(self.check_points[3]))

        if (abs(self.x[self.counter] - r_x) <1) and (abs(self.y[self.counter] - r_y) <1) and(abs(self.yaw[self.counter] - yaw_) <(20)):
            self.check_points[self.counter] = 1
            self.get_logger().info("I executed  {},{},{}".format(r_x,r_y,yaw_))

        

        if sum(self.check_points) == 4:
            self.get_logger().info("I executed all positions and the last one is {},{},{}".format(r_x,r_y,yaw_))


        self.counter +=1
        if self.counter == len(self.yaw):
            self.counter = 0

    def euler_from_quaternion(self, quaternion):
        x = quaternion.x
        y = quaternion.y
        z = quaternion.z
        w = quaternion.w

        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (w * y - z * x)
        pitch = np.arcsin(sinp)

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = np.arctan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw 


def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()