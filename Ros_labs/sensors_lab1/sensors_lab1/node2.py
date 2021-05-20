#!/usr/bin/env python3


import rclpy

from rclpy.node import Node 
from sensor_msgs.msg import Imu

import csv
from geometry_msgs.msg import Quaternion
from math import sin, cos, pi

   

class coor:
    def __init__(self):
        self.x = []
        self.y = []
        self.z = []
        
class Data:
    def __init__(self):
        self.linearAcc = coor()
        self.angularVel = coor()
        self.yaw = []
        
class my_client(Node):
    def __init__(self):
        super().__init__("node")
        self.sensor_data = Data()

        self.counter = 0
        self.imu_msg = Imu()
        self.imu_msg.header.frame_id= "zed2_imu_link"
        #self.imu_msg.header.stamp= Node.get_clock().now().to_msg()

        self.pub= self.create_publisher(Imu,"zed2_imu",rclpy.qos.qos_profile_sensor_data) 

        self.create_timer(1/30,self.timer_call)
        with open('/home/ahmed/ITI_ROS_WS/src/sensors_lab1/sensors_lab1/imu_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #accX, accY, accZ, angX, angY, angZ, yaw_deg
                self.sensor_data.linearAcc.x.append(float(list(row.values())[0]))
                self.sensor_data.linearAcc.y.append(float(list(row.values())[1]))
                self.sensor_data.linearAcc.z.append(float(list(row.values())[2]))

                self.sensor_data.angularVel.x.append(float(list(row.values())[3]))
                self.sensor_data.angularVel.y.append(float(list(row.values())[4]))
                self.sensor_data.angularVel.z.append(float(list(row.values())[5]))

                self.sensor_data.yaw.append(float(list(row.values())[6]))
        
        
    def timer_call(self):
        yaw = self.sensor_data.yaw[self.counter]
        accX = self.sensor_data.linearAcc.x[self.counter]
        accY = self.sensor_data.linearAcc.y[self.counter]
        accZ = self.sensor_data.linearAcc.z[self.counter]

        AngVelX = self.sensor_data.angularVel.x[self.counter]
        AngVelY = self.sensor_data.angularVel.y[self.counter]
        AngVelZ = self.sensor_data.angularVel.z[self.counter]

        cov_yaw = 0.000001
        cov_z   = 0.000001

        if abs(AngVelZ) > 0.3 :      
            cov_yaw *= (10*abs(AngVelZ))   # the covariance is directly proportional with the AngVelZ
            cov_z  *=  (10*abs(AngVelZ))
        
        
        self.imu_msg.orientation = self.quaternion_from_euler(0,0,yaw)
        
        self.imu_msg.orientation_covariance = [ 0.000001, 0.0, 0.0,
                                                0.0, 0.000001, 0.0, 
                                                0.0, 0.0, cov_yaw] #only yaw has covariance
        # angular velocity
        self.imu_msg.angular_velocity.x = AngVelX
        self.imu_msg.angular_velocity.y = AngVelY
        self.imu_msg.angular_velocity.z = AngVelZ
        self.imu_msg.angular_velocity_covariance=[   0.000001, 0.0, 0.0, 
                                                     0.0, 0.000001, 0.0,
                                                     0.0, 0.0, cov_z]  #only angular velocity z has covariance
        # linear acceleration
        self.imu_msg.linear_acceleration.x = accX
        self.imu_msg.linear_acceleration.y = accY
        self.imu_msg.linear_acceleration.z = accZ
        self.imu_msg.linear_acceleration_covariance=[0.000001, 0.0, 0.0,
                                                     0.0, 0.000001, 0.0,
                                                     0.0, 0.0, 0.000001]
        
        
        self.pub.publish(self.imu_msg)
        self.counter+=1
        if self.counter == len(self.sensor_data.yaw):
            self.counter = 0

    def quaternion_from_euler(self, roll, pitch, yaw):
        qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
        qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
        qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
        qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
        return Quaternion(x=qx, y=qy, z=qz, w=qw)



def main(args = None):
    rclpy.init(args=None)
    node = my_client()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()