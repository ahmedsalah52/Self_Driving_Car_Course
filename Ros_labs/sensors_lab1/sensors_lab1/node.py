#!/usr/bin/env python3


import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Imu
import numpy as np


class my_node(Node):
    def __init__(self):
        super().__init__("node")
   
        self.create_subscription(Imu,"/imu",self.sub_call,rclpy.qos.qos_profile_sensor_data) 
        self.get_logger().info("Subscriber is started now")

    def sub_call(self,msg):

        roll, pitch, yaw   = self.euler_from_quaternion(msg.orientation)
        if (abs(yaw) < 2):
            self.get_logger().info("The robot is nearly heading north .. Heading is: {} degrees".format(yaw))


        if abs(msg.linear_acceleration.x) > 0.3:
            self.get_logger().warn("Warning !! .. linear acceleration x exceeded the limit . Current acceleration is {} m/s^2“ where a is the current value".format(msg.linear_acceleration.x))
        
        if abs(msg.angular_velocity.z)> 0.3:
            self.get_logger().warn("Warning !! .. angular velocity z exceeded the limit . Current Angular velocity is {} rad/sec” where a is the current value".format(msg.angular_velocity.z))

        


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