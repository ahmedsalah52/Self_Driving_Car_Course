

#this node recieves a flag from control_node then make a new turtle_2 if flag equals true or kill it if false

import rclpy

from rclpy.node import Node 
from example_interfaces.msg import String ,Int64
from turtlesim.srv import Spawn
import random
from turtlesim.srv import Kill
from std_srvs.srv import Empty
from msgs.srv import FlagString

class my_node(Node):
    def __init__(self):
        super().__init__("spawn_node")
        self.flag = False
        self.get_logger().info("Spawn and server is started now")
        self.create_service(FlagString, 'server', self.srv_call)
        self.kill_turtle_client = self.create_client(Kill, "kill") 
        self.clear_client=self.create_client(Empty, "clear")

        #turtle sim client call
        self.client=self.create_client(Spawn, "spawn") #to spawn the Second turtle
        
        while self.client.wait_for_service(0.25) ==False:
            self.get_logger().warn("spawn node is waiting for turtlesim server")


   

    def future_call(self,future_msg):
        self.get_logger().info("Done")
   
   
   
    def srv_call(self,rq,rsp):
        if rq.flag == True:
            while self.client.wait_for_service(0.25) ==False:
                self.get_logger().warn("control waiting for new turtle server")

            rsp.message = "generating new turtle"
            request = Spawn.Request()
            request.x = float(random.randint(1,10))
            request.y  = float(random.randint(1,10))
            request.theta = 0.0
            request.name  = "turtle2"
            future_obj = self.client.call_async(request)
            future_obj.add_done_callback(self.future_call)
            
            
            
        else:
            while self.kill_turtle_client.wait_for_service(0.25) ==False:
                self.get_logger().warn("control waiting for kill server")
            self.get_logger().info("kill turtle")
            request = Kill.Request()
            request.name  = 'turtle2'
            future_obj = self.kill_turtle_client.call_async(request)
            
            while self.clear_client.wait_for_service(0.25) ==False:
                self.get_logger().warn("control waiting clear server")
            clear_request = Empty.Request()
            future_obj = self.clear_client.call_async(clear_request)



        self.get_logger().info(str(rq.flag))
        return rsp

  

        
        








  
def main(args = None):
    rclpy.init(args=None)
    node = my_node()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()