#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# --- 콜백 함수 3개 ---

def active_cb():
    """목표가 서버에서 활성화될 때 한 번 호출됩니다."""
    rospy.loginfo("[active] 목표 수신 완료, 이동 시작!")

def feedback_cb(feedback):  # 빈칸 9: feedback 객체를 받는 파라미터 이름
    """이동 중 주기적으로 호출됩니다. 현재 위치를 출력합니다."""
    x = feedback.base_position.pose.position.x  # 빈칸 10: feedback에서 현재 위치 x 추출
    y = feedback.base_position.pose.position.y
    rospy.loginfo("[feedback] 현재 위치: x=%.2f, y=%.2f", x, y)

def done_cb(state, result):
    """목표가 완료(성공/실패/취소)되면 호출됩니다."""
    if state == 3:
        rospy.loginfo("[done] 도착 성공!")
    else:
        rospy.logwarn("[done] 실패 (상태: %d)", state)

# --- 메인 ---

def send_goal_with_feedback():
    rospy.init_node('goal_with_feedback_node')

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("move_base 서버 대기중...")
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 1.5
    goal.target_pose.pose.position.y = 0.0
    goal.target_pose.pose.orientation.w = 1.0

    # 힌트: send_goal()의 키워드 인자로 콜백 3개를 연결하세요
    client.send_goal(  # 빈칸 11: send_goal 호출 + 콜백 연결
        goal,
        done_cb=done_cb,
        active_cb=active_cb,
        feedback_cb=feedback_cb
    )

    rospy.loginfo("목표 전송 완료. 콜백으로 상태를 수신합니다...")

    # 힌트: 블로킹 없이 ROS 이벤트 루프를 유지하는 방법
    while rospy.is_shutdown:  # 빈칸 12: 노드가 살아있는 동안 반복
        rospy.sleep(0.1)

if __name__ == '__main__':
    try:
        send_goal_with_feedback()
    except rospy.ROSInterruptException:
        pass
