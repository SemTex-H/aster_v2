import os

from ament_index_python.packages import get_package_share_directory
import xacro

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node


def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Process the URDF file
    try:
        pkg_path = os.path.join(get_package_share_directory('aster_v2'))
        xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
        
        # Process the XACRO file to generate URDF
        robot_description_config = xacro.process_file(xacro_file)
    except Exception as e:
        raise RuntimeError(f"Failed to process XACRO file {xacro_file}: {e}")
    
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}
    
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'
        ),
        node_robot_state_publisher
    ])
