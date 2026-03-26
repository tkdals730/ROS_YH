#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def create_goal(x, y):
    """좌표를 받아 MoveBaseGoal 메시지를 만듭니다."""
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1.0
    return goal

def patrol():
    rospy.init_node('patrol_node')

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("move_base 서버 대기중...")
    client.wait_for_server()

    # 힌트: Step 1에서 메모한 좌표. 예: (1.0, 0.0), (2.0, 1.0), (0.0, 0.0)
    waypoints = [(-0.01,1), (1,-0.02),(3.29,2.54)]  # 빈칸 6

    # 힌트: 프로그램이 종료되지 않는 한 계속 순찰
    while rospy.is_shutdown:  # 빈칸 7
        for i, (x, y) in enumerate(waypoints):
            goal = create_goal(x, y)
            rospy.loginfo("순찰 %d/%d: (%.1f, %.1f)로 이동",
                            i+1, len(waypoints), x, y)
            client.send_goal(goal)
            client.wait_for_result()

            # 힌트: 3이면 성공(SUCCEEDED) — 실습 3의 day06.md 상태코드표 참고
            state = client.get_state()  # 빈칸 8
            if state == 3:
                rospy.loginfo("도착 성공!")
            else:
                rospy.logwarn("실패 (상태: %d) - 다음 지점으로", state)

        rospy.loginfo("한 바퀴 완료! 다시 순찰 시작...")

if __name__ == '__main__':
    try:
        patrol()
    except rospy.ROSInterruptException:
        pass