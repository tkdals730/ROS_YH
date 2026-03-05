#!/usr/bin/env python3

import rospy
from beginner_tutorials.srv import AddTwoInts, AddTwoIntsResponse

def handle_calc(req):
    # 파라미터 서버에서 operator 읽기 (없으면 'add')
    op = rospy.get_param('/operator', 'add')

    if op == 'add':
        result = req.a + req.b

    elif op == 'sub':
        result = req.a - req.b

    elif op == 'mul':
        result = req.a * req.b

    else:
        rospy.logwarn("알 수 없는 연산: %s → 기본값 add 사용", op)
        result = req.a + req.b

    rospy.loginfo("[%s] %d, %d → %d", op, req.a, req.b, result)

    # AddTwoIntsResponse의 필드가 sum이지만,
    # 생성자는 결과값 하나만 넣으면 됩니다.
    return AddTwoIntsResponse(result)

def server():
    rospy.init_node('calc_server')

    # 서비스 이름: /calc (rosservice call /calc ...)
    rospy.Service('calc', AddTwoInts, handle_calc)

    rospy.loginfo("계산기 서버 시작 (operator 파라미터로 연산 변경)")
    rospy.spin()

if __name__ == '__main__':
    server()