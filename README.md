# ROS development
 Ubuntu 20.04
 Ros noetic

 # Ros install
 1. source list
 ```bash
 sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
 ```
 2. Set up your keys
 ```bash
sudo apt install curl # if you haven't already installed curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
```

3. apt update
```bash
sudo apt update
```
4.install full-version of noetic
```bash
sudo apt install ros-noetic-desktop-full
```
5.Environment setup
```bash
source /opt/ros/noetic/setup.bash
```

6.It can be convenient to automatically source this script every time a new shell is launched
```bash
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
```
7. Create a ROS Workspace
```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin_make
```
