from launch import LaunchDescription

import launch.actions
import launch_ros.actions


def generate_launch_description():    
    return LaunchDescription([
         
        launch_ros.actions.Node(
            package='turtlesim',
            executable='turtlesim_node',
            output='screen',
            arguments=[ ],
            ),
            
            
        launch_ros.actions.Node(
            package='iti_lab_9',
            executable='run',
            output='screen',
            arguments=[ ],
            ),



    ])
