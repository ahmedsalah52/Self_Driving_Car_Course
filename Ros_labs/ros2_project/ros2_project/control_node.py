#!/usr/bin/env python3
#!/usr/bin/env python3

#this node is responsible for moving turtle_1 to catch turtle_2 then send a flag to spawn_node to spawn a new turtle_2 or to kill it.

import rclpy

from rclpy.node import Node 
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
from std_srvs.srv import Empty
from msgs.srv import FlagString
class my_client(Node):
    def __init__(self):
        super().__init__("control_node")
        self.turtle_1_pos = [0.0,0.0,0.0] 
        self.turtle_2_pos = [0.0,0.0]
        self.flag = False

        self.service_client()
        self.create_timer(1/4,self.timer_call)

        self.create_subscription(Pose,"/turtle1/pose",self.sub_call_1,10) #to get the position of turtle_1 from topic /turtle1/pose
        self.create_subscription(Pose,"/turtle2/pose",self.sub_call_2,10) #to get the position of turtle_2

        self.turtle_1= self.create_publisher(Twist,"/turtle1/cmd_vel",10) # to publish the velocity to turtle_1 thats how we control turtle 1

    def service_client(self):
        self.client = self.create_client((FlagString), "server") #to send a flag to spawn node so that it spawn a new turtle or kills the old one according to the flag
        

        while self.client.wait_for_service(0.25) ==False:       #wait the server to be ready
            self.get_logger().warn("control waiting for spawn")
        
        self.get_new_turtle(True)    #spawn the first turtle_2
    
    
    
    

    def timer_call(self):
        delta_x = abs(self.turtle_1_pos[0] - self.turtle_2_pos[0])
        delta_y = abs(self.turtle_1_pos[1] - self.turtle_2_pos[1])
        
        accepted_error = 0.2
        if ((delta_x < accepted_error) and (delta_y < accepted_error)):  
            print("killing the turtle 2")
            
            self.stop_turtle_1()
            self.get_new_turtle(self.flag)
            self.flag = not self.flag
        
        else:
            print("moving turtle 1")

            self.Move_turtle_1()
        
    def Move_turtle_1(self):    
        x = self.turtle_1_pos[0]
        y = self.turtle_1_pos[1]
        yaw = self.turtle_1_pos[2] 

        x_goal = self.turtle_2_pos[0]
        y_goal = self.turtle_2_pos[1]
        
        k_linear = 1.0
        distance = abs(math.sqrt(((x_goal-x)**2)+((y_goal-y)**2)))
        linear_speed = distance * k_linear

        
        k_angular = 4.0
        desired_angle_goal = math.atan2(y_goal-y,x_goal-x)
        angular_speed = (desired_angle_goal - yaw) * k_angular
        
        
        
        velocity = Twist()
        velocity.linear.x = linear_speed
        velocity.angular.z = angular_speed

        self.turtle_1.publish(velocity)
    
    
    def sub_call_1(self,msg):
        self.turtle_1_pos[0] = msg.x
        self.turtle_1_pos[1] = msg.y
        self.turtle_1_pos[2] = msg.theta


    def sub_call_2(self,msg):
        self.turtle_2_pos[0] = msg.x
        self.turtle_2_pos[1] = msg.y

    def stop_turtle_1(self):
        velocity = Twist()
        velocity.linear.x = 0.0
        velocity.angular.z = 0.0
        self.turtle_1.publish(velocity)
    


    def get_new_turtle(self,get_or_kill):
        while self.client.wait_for_service(0.25) ==False:
            self.get_logger().warn("control waiting for new turtle server")
        self.get_logger().info("Get new turtle")

        request = FlagString.Request()
        request.flag = get_or_kill
        future_obj = self.client.call_async(request)
        future_obj.add_done_callback(self.future_call)

    def future_call(self,future_msg):
        self.incoming_msg = future_msg.result().message
        self.get_logger().info(str(future_msg.result().message))
       

def main(args = None):
    rclpy.init(args=None)
    node = my_client()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()
