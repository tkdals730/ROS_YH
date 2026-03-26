#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def send_goal():
    rospy.init_node('send_goal_node')

    # actionlib 클라이언트 생성
    # 힌트: Navigation의 핵심 노드 이름은?
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)  # 빈칸 1
    rospy.loginfo("move_base 서버 대기중...")
    client.wait_for_server()
    rospy.loginfo("서버 연결 완료!")

    goal = MoveBaseGoal()

    # 힌트: 실습 1에서 확인한 /odom의 frame_id가 아닌, 지도의 좌표계
    goal.target_pose.header.frame_id = "map"  # 빈칸 2
    goal.target_pose.header.stamp = rospy.Time.now()

    # 힌트: RViz에서 목표 지점에 마우스를 올리면 하단에 좌표가 표시됨
    goal.target_pose.pose.position.x = 2.0  # 빈칸 3
    goal.target_pose.pose.position.y = 0.0

    # 힌트: 실습 1에서 배운 쿼터니언 — 회전 없이 정면을 보려면?
    goal.target_pose.pose.orientation.w = 1.0  # 빈칸 4

    rospy.loginfo("목표 전송: x=%.1f, y=%.1f",
                    goal.target_pose.pose.position.x,
                    goal.target_pose.pose.position.y)
    client.send_goal(goal)  # 빈칸 5

    client.wait_for_result()
    rospy.loginfo("결과: %s", client.get_state())

if __name__ == '__main__':
    try:
        send_goal()
    except rospy.ROSInterruptException:
        pass
