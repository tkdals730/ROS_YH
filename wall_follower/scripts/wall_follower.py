#!/usr/bin/env python3
import rospy
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# ===== 파라미터 =====
LINEAR_SPEED = 0.15
ANGULAR_SPEED = 0.3
DESIRED_DISTANCE = 0.5  # 벽에서 유지할 거리 (m)

class WallFollowerPID:
    def __init__(self):
        rospy.init_node('wall_follower_pid')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        # PID 게인
        self.kp = 1.0 # 1.0 진동있음
        self.ki = 0.0
        self.kd = 0.1

        # PID 상태
        self.integral = 0.0
        self.prev_error = 0.0
        self.dt = 0.1  # 10Hz

        self.rate = rospy.Rate(10)

    def get_range(self, scan, angle):
        index = int((angle - scan.angle_min) / scan.angle_increment)
        index = max(0, min(index, len(scan.ranges) - 1))
        distance = scan.ranges[index]
        if math.isnan(distance) or math.isinf(distance):
            distance = 10.0
        return distance

    def get_error(self, scan, desired_distance):
        theta = math.radians(45)
        a = self.get_range(scan, -math.radians(45))
        b = self.get_range(scan, -math.radians(90))
        alpha = math.atan2(a * math.cos(theta) - b, a * math.sin(theta))
        wall_distance = b * math.cos(alpha)
        return desired_distance - wall_distance

    def pid_control(self, error):
        p_term = self.kp * error
        self.integral += error * self.dt
        i_term = self.ki * self.integral
        d_term = self.kd * (error - self.prev_error) / self.dt
        self.prev_error = error

        angular_z = p_term + i_term + d_term

        twist = Twist()
        twist.linear.x = LINEAR_SPEED
        twist.angular.z = angular_z
        self.pub.publish(twist)

    def scan_callback(self, scan):
        front = self.get_range(scan, 0.0)
        error = self.get_error(scan, DESIRED_DISTANCE)

        if front < 0.5:
            twist = Twist()
            twist.angular.z = ANGULAR_SPEED
            self.pub.publish(twist)
            rospy.loginfo("전방 벽 — 좌회전 | 전방: %.2f", front)
        else:
            self.pid_control(error)
            rospy.loginfo("PID 벽 따라가기 | 오차: %.3f", error)

if __name__ == '__main__':
    try:
        wf = WallFollowerPID()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass