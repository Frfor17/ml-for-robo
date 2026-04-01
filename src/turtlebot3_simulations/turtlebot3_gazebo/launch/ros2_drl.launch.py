import os
print(f"🔍 LAUNCH DEBUG: TURTLEBOT3_MODEL={os.environ.get('TURTLEBOT3_MODEL', 'NOT SET')}")
print(f"🔍 World path: {world}")

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

TURTLEBOT3_MODEL = os.environ["TURTLEBOT3_MODEL"]


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time", default="true") # sync robot clock with gazebo
    pause = LaunchConfiguration("pause", default="false") # wtf, robot runs immediately
    world_file_name = "turtlebot3_drl/" + TURTLEBOT3_MODEL + ".model" # "turtlebot3_drl/waffle_pi.model" but its working... strange... there is empty map
    world = os.path.join(
        get_package_share_directory("turtlebot3_gazebo"), "worlds", world_file_name # finding package folder?
    )
    launch_file_dir = os.path.join( # wtf is that, xz, i dont know, some paths
        get_package_share_directory("turtlebot3_gazebo"), "launch"
    )
    pkg_gz_sim = get_package_share_directory("ros_gz_sim")

    return LaunchDescription(
        [
                LogInfo(msg=[
                '🔍 LAUNCH DEBUG: TURTLEBOT3_MODEL=', 
                os.environ.get('TURTLEBOT3_MODEL', 'NOT SET')
                ]),
                LogInfo(msg=['🔍 World path: ', world]),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(pkg_gz_sim, "launch", "gz_sim.launch.py") #seems like launching GAZEBO 3D SIMULATION??
                ),
                launch_arguments={"world": world, "pause": pause}.items(), # giving params(world file + pause setts), MAYBE, I DONT KNOW
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [launch_file_dir, "/robot_state_publisher.launch.py"] # SOME PUBLISHER... of robot.. some robot joints?
                ),
                launch_arguments={"use_sim_time": use_sim_time}.items(), # some params
            ),
        ]
    )
