#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def main():

    rospy.init_node('circle_publisher')

    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        msg = Twist()

        msg.linear.x = 2.0 # 이동속도
        msg.angular.z = 1.0 # 방향전환 속도

        pub.publish(msg)

        rate.sleep()

if __name__ == '__main__':
    main()