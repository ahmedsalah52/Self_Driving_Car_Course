from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped

class StatePublisher(Node):

    def __init__(self):
        rclpy.init()
        super().__init__('state_publisher')

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))

        degree = pi / 180.0
        loop_rate = self.create_rate(30)

        # robot state
        
        angle = 0.0
       
        direction = 1
        # message declarations
        lidar_servo = TransformStamped()
        lidar_servo.header.frame_id = 'servo'
        lidar_servo.child_frame_id = 'lidar2'
        joint_state = JointState()

        try:
            while rclpy.ok():
                rclpy.spin_once(self)

                # update joint_state
                now = self.get_clock().now()
                joint_state.header.stamp = now.to_msg()
                joint_state.name = ['swivel', 'tilt', 'periscope']
                #joint_state.position = [swivel, tilt, height]

                # update transform
                # (moving in a circle with radius=2)
                lidar_servo.header.stamp = now.to_msg()
                lidar_servo.transform.translation.x = 0.0
                lidar_servo.transform.translation.y =  0.0
                lidar_servo.transform.translation.z =  0.0
                lidar_servo.transform.rotation = \
                    euler_to_quaternion(0,  (angle*pi)/180 ,0) # roll,pitch,yaw
                
                # send the joint state and transform
                self.joint_pub.publish(joint_state)
                self.broadcaster.sendTransform(lidar_servo)

                # Create new robot state
                limit = 30
                if angle >= limit:
                    direction = -1
                elif angle <= -limit:
                    direction = 1

                angle += (0.5*direction)
                print((angle*pi)/180)
                # This will adjust as needed per iteration
                loop_rate.sleep()

        except KeyboardInterrupt:
            pass

def euler_to_quaternion(roll, pitch, yaw):
    qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
    qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
    qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
    qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
    return Quaternion(x=qx, y=qy, z=qz, w=qw)

def main():
    node = StatePublisher()

if __name__ == '__main__':
    main()