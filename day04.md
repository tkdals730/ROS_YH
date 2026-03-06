# Day 4: ROS Action을 이용한 타이머 구현 및 비동기 통신 이해

## 1. ROS 통신 방식의 차이점 요약
ROS의 주요 통신 방식인 Topic, Service, Action의 구조적 차이를 정리합니다.

| 구분 | Topic (토픽) | Service (서비스) | Action (액션) |
| :--- | :--- | :--- | :--- |
| **통신 방식** | 단방향 (Pub-Sub) | 양방향 (Req-Res) | 양방향 (Goal-Feedback-Result) |
| **특징** | 연속적인 데이터 스트림 | 일시적 요청/빠른 응답 | **장시간 수행되는 작업**에 적합 |
| **피드백** | 없음 | 없음 | **작업 중 실시간 진행 상황 공유** |
| **중도 취소** | 불가능 | 불가능 | **작업 수행 중 취소(Cancel) 가능** |

---

## 2. 패키지 환경 설정

### ① package.xml 수정
`actionlib`와 `actionlib_msgs` 의존성을 추가합니다.

```xml
<build_depend>actionlib</build_depend>
<build_depend>actionlib_msgs</build_depend>
<exec_depend>actionlib</exec_depend>
<exec_depend>actionlib_msgs</exec_depend>
```
---
# 3. CMakeLists.txt 수정
빌드 시스템이 액션 파일을 인식하도록 5개 항목을 수정합니다.
## 3-1. find_package에 구성 요소 추가
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  actionlib
  actionlib_msgs
)

## 3-2. 액션 파일 등록 (Timer.action)
add_action_files(
  FILES
  Timer.action
)

## 3-3. 메시지 생성 의존성 설정
generate_messages(
  DEPENDENCIES
  std_msgs
  actionlib_msgs
)

## 3-4. 패키지 런타임 의존성 선언
catkin_package(
  CATKIN_DEPENDS actionlib_msgs
)

## 3-5. 파이썬 스크립트 설치 등록 (scripts 폴더 내 파일들)
```
catkin_install_python(
  PROGRAMS
  scripts/timer_server.py
  scripts/timer_client.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
```
---
# 4. 액션 인터페이스 정의 (Timer.action)
서비스와 달리 세 부분(Goal, Result, Feedback)으로 구성된 인터페이스 파일을 생성합니다.

Bash
## 1. action 폴더 생성
mkdir -p ~/catkin_ws/src/beginner_tutorials/action

## 2. Timer.action 파일 생성 및 편집
nano ~/catkin_ws/src/beginner_tutorials/action/Timer.action

### 1. Goal: 클라이언트가 서버에 요청할 내용 (목표 시간)
duration duration
---
### 2. Result: 작업 완료 후 최종 반환값 (총 소요 시간)
duration time_elapsed
uint32 updates_sent
---
### 3. Feedback: 작업 진행 중 실시간 보고 내용 (남은 시간 등)
duration time_elapsed
duration time_remaining

--- 
# 5. 빌드 및 실행 권한 부여
① 워크스페이스 빌드
설정 파일을 수정한 후에는 반드시 빌드를 통해 메시지 파일을 생성해야 합니다.

```Bash
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

# 자동 생성된 액션 메시지 구조 확인 (TimerAction 포함 7개 확인)
```
rosmsg list | grep Timer
```

② 실행 권한 부여
---
작성한 서버와 클라이언트 스크립트에 실행 권한을 부여합니다.

```Bash
chmod +x ~/catkin_ws/src/beginner_tutorials/scripts/timer_server.py
chmod +x ~/catkin_ws/src/beginner_tutorials/scripts/timer_client.py
```

---
# 6. 실행 및 외부 취소 테스트
왜 외부에서 취소 명령을 실행하나요?
서버 안정성 검토: 서버 노드(timer_server.py)가 작업 중에도 외부 신호를 실시간으로 감지(is_preempt_requested)하는지 확인합니다.

비동기 통신 확인: 요청을 보낸 클라이언트가 아닌 제3의 터미널에서도 작업을 제어할 수 있는 ROS 액션의 특징을 테스트합니다.

# 실행방법
터미널1
```bash
roscore 실행
```
터미널2
```bash
rosrun beginner_tutorials timer_server.py
```
터미널3
```bash
rosrun beginner_tutorials timer_client.py 100
```
100초동안 실행
---
### 6-1. 취소용 메시지 타입 확인

```Bash
rosmsg show actionlib_msgs/GoalID
```
### 6-2. 취소 토픽 발행 (Cancel)

```Bash
rostopic pub /timer/cancel actionlib_msgs/GoalID -- {}
```

결과 확인: 명령어가 입력되는 즉시 서버 터미널에 "타이머 취소됨!" 로그가 출력되며 작업이 안전하게 중단되는지 확인합니다.
---

