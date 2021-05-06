from launch import LaunchDescription

import launch.actions
import launch_ros.actions


def generate_launch_description():    
    return LaunchDescription([
        
        launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            output='screen',
            arguments=['0', '0', '1.77', '0', '0', '0','base_footprint' ,'gps_link' ],
            ),

         launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            output='screen',
            arguments=['1.92', '0', '0.36', '0', '0', '0','base_footprint', 'lidar_link' ],
            ),

   launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            output='screen',
            arguments=['1.8', '0.3', '1', '0', '0', '0','base_footprint', 'zed2_link' ],
            ),

   launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            output='screen',
            arguments=['-0.1', '0', '0.88', '3.14', '0', '0','base_footprint', 'mynt_link' ],
            ),

   launch_ros.actions.Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            output='screen',
            arguments=['1.8', '0.5', '1', '0', '0', '0','base_footprint', 'imu_link' ],
            ),

    ])
