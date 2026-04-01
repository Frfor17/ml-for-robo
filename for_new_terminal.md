for new terminal:

FIRST:
------------------------------------------------------------
# Add to ~/.bashrc (one time only)
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
echo "source ~/ml-for-robo/install/setup.bash" >> ~/.bashrc
echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc

# Reload
source ~/.bashrc
---------------------------------------------------------------

SECOND:
-----------------------------------------------
# New terminal → instantly:
ros2 pkg list | grep turtlebot3_gazebo  # Should show package
ros2 launch turtlebot3_gazebo ros2_drl.launch.py  # Launches sim!
--------------------------------------------




FOR EXTRA KEYS(MAYBE WILL HELP IF ALL GONE WRONG):
------------------------------------------
# 3-line combo that always works:
source /opt/ros/jazzy/setup.bash
source ~/ml-for-robo/install/setup.bash  
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo ros2_drl.launch.py
-----------------------------------------