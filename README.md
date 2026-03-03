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

6.It can be convenient to automatically source this script every time a new shell is launched.These commands will do that for you.
```bash
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
```
7. Create a ROS Workspace
```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
catkin_make
```
# 터틀 필드 분석
```bash
roscore  #마스터
새 터미널 실행 
rosrun turtlesim turtlesim_node #프로그램 실행 노드
새 터미널 실행    
rosrun turtlesim turtle_teleop_key # 방향키 이동 
새 터미널 실행
rostopic echo /turtle1/pose # 이동 좌표등등

```
실행결과:\
x: 5.544444561004639   #좌우로 이동시 변경\
y: 5.544444561004639   #상하로 이동시 변경\
theta: 0.0             #바라보는 방향?각도?\
linear_velocity: 0.0   #이동속도 이동시 2.0\
angular_velocity: 0.0   #회전속도 

#토픽 메시지 목록 타입 구조
```bash
#토픽리스트
$ rostopic list
/turtle1/cmd_vel
/turtle1/color_sensor
/turtle1/pose
# 토픽메시지 타입
$ rostopic type /turtle1/cmd_vel
geometry_msgs/Twist
$ rostopic type /turtle1/color_sensor
turtlesim/Color
$ rostopic type /turtle1/pose
turtlesim/Pose
#구조
$ rosmsg show geometry_msgs/Twist
geometry_msgs/Vector3 linear
float64 x
float64 y
float64 z
geometry_msgs/Vector3 angular
float64 x
float64 y
float64 z

$ rosmsg show turtlesim/Color
uint8 r
uint8 g
uint8 b

$ rosmsg show turtlesim/Color
float32 x
float32 y
float32 theta
float32 linear_velocity
float32 angular_velocity

```