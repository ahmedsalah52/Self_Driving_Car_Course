# Sa3eed mohamed zaid
# mohamed abd el fata7 
# mohamed tariq sedky
# ahmed salah 
        
import rclpy

from rclpy.node import Node 
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import serial

#from std_srvs.srv import Empty
#from msgs.srv import FlagString
class my_client(Node):
    def __init__(self):
        super().__init__("control_node")
        print('hello')

        self.set_point_vel = [0.0,0.0] 

        self.flag = False
        self.sample_time = 1/10
        self.right_cum_error  = 0.0
        self.right_Rate_error = 0.0
        self.right_prev_error = 0.0

        self.left_cum_error  = 0.0
        self.left_Rate_error = 0.0
        self.left_prev_error = 0.0
        
        self.create_timer(self.sample_time,self.timer_call)

        self.create_subscription(Twist,'/cmd_vel',self.set_vel,10) #to get the position of turtle_1 from topic /turtle1/pose


        self.pub_vel= self.create_publisher(Twist,"out_vel",10) # to publish the velocity to turtle_1 thats how we control turtle 1
        self.arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1) #change 

    

    def timer_call(self):
        

        print("timer start")
        self.arduino.flush()
        data = self.arduino.readline().decode('ascii').split(',')
        #data = data_str.split(",")
        if len(data)<2:
            return
        V_left_feedback = float(data[1])   #m/s
        V_right_feedback = float(data[2]) #m/s

        
        linear_setpoint = self.set_point_vel[0]
        angular_setpoint = self.set_point_vel[1]

        distance_wheels = 0.58
        R_set = linear_setpoint +((angular_setpoint * distance_wheels)/2)
        L_set = linear_setpoint - ((angular_setpoint * distance_wheels)/2)

        # right pid section
        k_p = 130
        k_i = 25
        k_d = 10

       
        right_error = R_set - V_right_feedback
        #print("from : {},{}, to {},{} with error: {}".format(x,y,x_goal,y_goal,linear_error))

        self.right_cum_error += (right_error * self.sample_time)
        self.right_Rate_error = (right_error- self.right_prev_error)/self.sample_time
        self.right_prev_error = right_error
        if self.right_cum_error > 255/k_i:
            self.right_cum_error= 255/k_i
        P = k_p * right_error
        I = k_i * self.right_cum_error
        
        D = k_d * self.right_Rate_error
        right_speed = P + I + D

      



        left_error = (L_set - V_left_feedback)

        self.left_cum_error += (left_error * self.sample_time)
        self.left_Rate_error = (left_error- self.left_prev_error)/self.sample_time
        self.left_prev_error = left_error
        if self.left_cum_error > 255/k_i:
            self.left_cum_error = 255/k_i
        P = k_p * left_error
        I = k_i * self.left_cum_error
        
        D = k_d * self.left_Rate_error
        left_speed = P + I + D

        
        #print("speeds : {},{}".format(linear_speed,angular_speed ))

        

        if left_speed >255 :
            left_speed = 255

        if left_speed < -255 :
            left_speed = -255
    
        if right_speed >255 :
            right_speed = 255

        if right_speed < -255 :
            right_speed  = -255
    
        #if(( abs(left_speed) > 255)or ( abs(right_speed) > 255)):
        #    if abs(left_speed) > abs(right_speed):
         #       right_speed = (right_speed/left_speed) * 255
          #      left_speed = 255
           # else:
            #    left_speed = (left_speed/right_speed) * 255
             #   right_speed = 255

        
        self.arduino.write(("{},{}").format(int(left_speed),int(right_speed)).encode())


        
        print("setpoint : {},{}".format(L_set,R_set ))

        print("command  : {},{}".format(V_left_feedback,V_right_feedback ))
        velocity = Twist()
        velocity.linear.x = L_set
        velocity.linear.z = R_set

        self.pub_vel.publish(velocity)
        print("timer end")


    
    def set_vel(self,msg):
        self.set_point_vel[0] = msg.linear.x
        self.set_point_vel[1] = msg.angular.z



        

    def stop_turtle_1(self):
        velocity = Twist()
        velocity.linear.x = 0.0
        velocity.angular.z = 0.0
        self.turtle_1.publish(velocity)
       

def main(args = None):
    rclpy.init(args=None)
    node = my_client()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
