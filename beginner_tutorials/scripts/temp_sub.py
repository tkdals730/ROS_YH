#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32

def callback(msg):

    temp = msg.data

    if temp >= 35.0:
        rospy.logwarn("⚠️ 경고! 온도 높음: %.2f", temp)
    else:
        rospy.loginfo("온도 정상: %.2f", temp)

def listener():

    rospy.init_node('temperature_subscriber')

    rospy.Subscriber('temperature', Float32, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
