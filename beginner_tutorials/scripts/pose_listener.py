#!/usr/bin/env python3

import rospy

from turtlesim.msg import Pose

def callback(msg):

    rospy.loginfo("위치: x=%.2f, y=%.2f, 방향=%.2f", msg.x, msg.y, msg.theta)

def listener():

    rospy.init_node('pose_listener')

    rospy.Subscriber('/turtle1/pose', Pose, callback)

    rospy.spin()

if __name__ == '__main__':

    listener()
