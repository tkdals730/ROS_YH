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

3. Installation
```bash
sudo apt update
```
4.Desktop-Full Install
```bash
Desktop-Full Install
```
5.Environment setup
```bash
source /opt/ros/noetic/setup.bash
'''
6.
```bash
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
```