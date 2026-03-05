#!/usr/bin/env python3

import rospy

from turtlesim.srv import SetPen

def change_pen(r, g, b, width):

    rospy.wait_for_service('/turtle1/set_pen')

    try:

        set_pen = rospy.ServiceProxy('/turtle1/set_pen', SetPen)

        set_pen(r, g, b, width, 0)

        rospy.loginfo("펜 변경: R=%d G=%d B=%d 두께=%d", r, g, b, width)

    except rospy.ServiceException as e:

        rospy.logerr("실패: %s", e)

if __name__ == '__main__':

    rospy.init_node('change_pen_client')

    change_pen(0, 255, 0, 5)    # 초록색, 두께 5
