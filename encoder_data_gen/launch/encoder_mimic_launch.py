from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='encoder_data_gen',
            executable='encoder_data_node',
            name='encoder_data_node',
            output='screen'
        )
    ])