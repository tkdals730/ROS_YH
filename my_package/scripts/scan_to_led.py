#!/usr/bin/env python3
import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

class LedDecisionNode:
    def __init__(self):
        rospy.init_node('led_decision_node')
        self.led_pub = rospy.Publisher('/led_color', String, queue_size=1)
        self.cmd_sub = rospy.Subscriber('/cmd_vel', Twist, self.cmd_callback)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)

        self.current_linear_x = 0.0
        self.front_distance = 10.0

    def publish_led(self, color):
        msg = String()
        msg.data = color
        self.led_pub.publish(msg)

    def get_front_distance(self, scan):
        index = int((0.0 - scan.angle_min) / scan.angle_increment)
        index = max(0, min(index, len(scan.ranges) - 1))
        distance = scan.ranges[index]

        if math.isnan(distance) or math.isinf(distance):
            distance = 10.0

        return distance

    def cmd_callback(self, msg):
        self.current_linear_x = msg.linear.x
        self.update_led()

    def scan_callback(self, scan):
        self.front_distance = self.get_front_distance(scan)
        self.update_led()

    def update_led(self):
        # Highest priority: obstacle is close
        if self.front_distance < 0.3:
            self.publish_led("red")
        else:
            if self.current_linear_x > 0.0:
                self.publish_led("green")
            elif self.current_linear_x < 0.0:
                self.publish_led("blue")
            else:
                self.publish_led("off")

if __name__ == '__main__':
    try:
        node = LedDecisionNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass