#!/usr/bin/env python3

import rospy
import random
from std_msgs.msg import Float32

def talker():

    rospy.init_node('temperature_publisher')

    pub = rospy.Publisher('temperature', Float32, queue_size=10)

    rate = rospy.Rate(1)   # 1초

    while not rospy.is_shutdown():

        temp = random.uniform(20.0, 40.0)

        rospy.loginfo("온도 발행: %.1f", temp)

        pub.publish(temp)

        rate.sleep()

if __name__ == '__main__':
    talker()
