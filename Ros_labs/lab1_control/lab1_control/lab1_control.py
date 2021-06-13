
        
import rclpy

from rclpy.node import Node 
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
#from std_srvs.srv import Empty
#from msgs.srv import FlagString
class my_client(Node):
    def __init__(self):
        super().__init__("control_node")
        print('hello')

        self.turtle_1_pos = [0.0,0.0,0.0] 
        self.turtle_2_pos = [9.0,9.0,0.0] 

        self.flag = False
        self.sample_time = 1/16
        self.distance_cum_error  = 0.0
        self.distance_Rate_error = 0.0
        self.distance_prev_error = 0.0

        self.angle_cum_error  = 0.0
        self.angle_Rate_error = 0.0
        self.angle_prev_error = 0.0
        
        self.create_timer(self.sample_time,self.timer_call)

        self.create_subscription(Pose,"/turtle1/pose",self.sub_call_1,10) #to get the position of turtle_1 from topic /turtle1/pose


        self.turtle_1= self.create_publisher(Twist,"/turtle1/cmd_vel",10) # to publish the velocity to turtle_1 thats how we control turtle 1
    
    

    def timer_call(self):
        delta_x = abs(self.turtle_1_pos[0] - self.turtle_2_pos[0])
        delta_y = abs(self.turtle_1_pos[1] - self.turtle_2_pos[1])
        distance_error = abs(math.sqrt(((delta_x)**2)+((delta_y)**2)))

        accepted_error = 0.01
        if (distance_error < accepted_error):  
            print("reached the target")
            
            self.stop_turtle_1()
            self.distance_cum_error = 0.0
            self.angle_cum_error = 0.0
        else:
            print("moving turtle")
            self.Move_turtle_1()
        
    def Move_turtle_1(self):    
        x = self.turtle_1_pos[0]
        y = self.turtle_1_pos[1]
        yaw = self.turtle_1_pos[2] 

        x_goal = self.turtle_2_pos[0]
        y_goal = self.turtle_2_pos[1]


        # distance pid section
        k_p = 0.2
        k_i = 0.01
        k_d = 0.08

        #k_p = 0.15
        #k_i = 0.06
        #k_d = 0.1

        distance_error = abs(math.sqrt(((x_goal-x)**2)+((y_goal-y)**2)))
        print("from : {},{}, to {},{} with error: {}".format(x,y,x_goal,y_goal,distance_error))

        self.distance_cum_error += (distance_error * self.sample_time)
        self.distance_Rate_error = (distance_error- self.distance_prev_error)/self.sample_time
        self.distance_prev_error = distance_error
        P = k_p * distance_error
        I = k_i * self.distance_cum_error
        D = k_d * self.distance_Rate_error
        linear_speed = P + I + D



        # angle pid section 
        k_p = 1
        k_i = 0.075
        k_d = 0.05

        #k_p = 0.5
        #k_i = 0.6
        #k_d = 0.1

        desired_angle_goal = math.atan2(y_goal-y,x_goal-x)
        angle_error = (desired_angle_goal - yaw)

        self.angle_cum_error += (angle_error * self.sample_time)
        self.angle_Rate_error = (angle_error- self.angle_prev_error)/self.sample_time
        self.angle_prev_error = angle_error
        P = k_p * angle_error
        I = k_i * self.angle_cum_error
        D = k_d * self.angle_Rate_error
        angular_speed = P + I + D

        
        velocity = Twist()
        velocity.linear.x = linear_speed
        velocity.angular.z = angular_speed

        self.turtle_1.publish(velocity)
    
    
    def sub_call_1(self,msg):
        self.turtle_1_pos[0] = msg.x
        self.turtle_1_pos[1] = msg.y
        self.turtle_1_pos[2] = msg.theta



        

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