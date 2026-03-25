#!/usr/bin/env python3
import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# ===== Parameters =====
LINEAR_SPEED = 0.15 # 직진속도(m/s)
ANGULAR_SPEED = 0.7 # 회전속도(rad/s)
DESIRED_DISTANCE = 0.5 # 벽과 유지할 거리(m)
FRONT_THRESHOLD = 0.35 # 앞에 벽이 있다고 판단하는 거리 

class WallFollowerPID:
    def __init__(self):
        rospy.init_node('wall_follower_pid')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        # PID 제어 변수
        self.kp = 0.5  # 현재 오차에 비례하여 보정하는 게인. 값이 크면 진동할수 있습니다.(0.3~1)
        self.ki = 0.01
        self.kd = 0.7  # 오차의 변화율을 보고 브레이크를 거는 게인입니다. (0.1~1)

        self.integral = 0.0
        self.prev_error = 0.0
        self.dt = 0.1

        self.rate = rospy.Rate(10)

        # rosy.info로 시작시 파라미터 출력
        rospy.loginfo("DESIRED_DISTANCE:%.2f", DESIRED_DISTANCE)
        rospy.loginfo("PID: kp=%.2f ki=%.2f kd=%.2f", self.kp, self.ki, self.kd)
    # 주어진 각도(라디안)에서 Lidar거리를 반환합니다.
    def get_range(self, scan, angle):
        index = int((angle - scan.angle_min) / scan.angle_increment)
        index = max(0, min(index, len(scan.ranges) - 1))
        distance = scan.ranges[index]
        if math.isnan(distance) or math.isinf(distance):
            distance = 10.0
        return distance
    # 오른쪽 벽까지의 거리 오차를 계산합니다.
    def get_error(self, scan, desired_distance):
        theta = math.radians(45)
        a = self.get_range(scan, math.radians(314)) #-45도의 lidar값을 측정
        b = self.get_range(scan, math.radians(270)) # -90의 Lida값을 측정 
        alpha = math.atan2(a * math.cos(theta) - b, a * math.sin(theta)) 
        wall_distance = b * math.cos(alpha) # 수직거리 계산
        return desired_distance - wall_distance # 오차 = 원하는 거리 - 실제거리 
    # PID 제어로 회전 속도를 계산하고 로봇을 움직입ㄴ다. 
    def pid_control(self, error):
        # P(비례) : 오차가 크면 크게 보정 
        p_term = self.kp * error
        self.integral += error * self.dt
        self.integral = max(-1.0, min(1.0, self.integral))
        # I( 적분) : 오차가 쌓이면 보정 
        i_term = self.ki * self.integral
        # D(미분) : 오차가 급변하면 브레이크 
        d_term = self.kd * (error - self.prev_error) / self.dt
        self.prev_error = error
        # 최종 회전 속도 
        angular_z = p_term + i_term + d_term

        twist = Twist()
        twist.linear.x = LINEAR_SPEED
        twist.angular.z = angular_z
        self.pub.publish(twist)
    # Lidar 데이터가 올 떄마다 실행된다. 
    def scan_callback(self, scan):
        # 전방 장애물 감지(정면)
        front = self.get_range(scan, 0.0)
        # 전방 장애물 감지(좌측 20도)
        front_left = self.get_range(scan, math.radians(20))
        # 전방 장애물 감지(우측 20도)
        #front_right = self.get_range(scan, -math.radians(20))
        front_right = self.get_range(scan, math.radians(340))
        #left = self.get_range(scan, math.radians(90))
        #right = self.get_range(scan, -math.radians(90))
        min_front = min(front, front_left, front_right)
        
        right = self.get_range(scan, math.radians(270))
        # 앞에 벽이 있으면 : 천천히 전진하면서 왼쪽으로 회전 
        twist = Twist()
        if min_front < FRONT_THRESHOLD:
            #twist = Twist()
            #twist.linear.x = 0.05 #아주 느린 속도로 전진한다
            twist.linear.x = 0.0 #제자리 왼쪽 회전  
            twist.angular.z = ANGULAR_SPEED # 왼쪽 회전 
            self.pub.publish(twist)
            rospy.loginfo("TURN | front: %.2f right: %.2f", min_front, right)
        elif right > DESIRED_DISTANCE * 2.5:
            twist.linear.x = LINEAR_SPEED
            twist.angular.z = -0.3
            self.pub.publish(twist)
            rospy.loginfo("SEARCH | fron: %.2f right: %.2f", min_front, right)
        else:
            # 벽 따라간다 (PID)
            error = self.get_error(scan, DESIRED_DISTANCE)
            self.pid_control(error)
            rospy.loginfo("FOLLOW | error: %.3f front: %.2f", error, min_front)
        # 디버깅
        rospy.loginfo_once("angle_min=%.3f angle_max=%.3f samples=%d", scan.angle_min, scan.angle_max, len(scan.ranges))
        right_dist = self.get_range(scan, math.radians(270))
        rospy.loginfo("right_wall=%.2f", right_dist)
if __name__ == '__main__':
    try:
        wf = WallFollowerPID()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass