import math
import threading
import time

from typing import Optional
import mediapipe as mp
import cv2
import numpy as np
import pyautogui


def judgeAngles(angle, result_post) -> bool:
    """
    判断动作角度是否符合要求

    :param angle:
    :param result_post:
    :return:
    """
    post1 = result_post.landmark[int(angle.organ1)]
    post2 = result_post.landmark[int(angle.organ2)]
    post3 = result_post.landmark[int(angle.organ3)]
    post4 = result_post.landmark[int(angle.organ4)]

    min_angle = int(angle.angle1)
    max_angle = int(angle.angle2)

    result_angle = get_angle(post1, post2, post3, post4)
    # print("角度:")
    # print("最小:"+str(min_angle))
    # print("最大:" + str(max_angle))
    # print(result_angle)
    return bool(min_angle <= result_angle <= max_angle)


def judgePosition(position, result_post) -> bool:
    """
    判断动作关键位置是否符合要求

    :param position:
    :param result_post:
    :return:
    """
    standard_post = result_post.landmark[int(position.standard)]
    if standard_post.visibility <= 0.1:
        return False
    input_judge_point = position.judge_point.split("|")
    for left_post in input_judge_point:
        judge_post = result_post.landmark[int(left_post)]
        if judge_post.visibility <= 0.1:
            return False
        print("标准：")
        print(int(position.standard))
        print(standard_post)
        print("判断：")
        print(int(left_post))
        print(judge_post)
        if position.located == "左":
            # print("zuo")
            if judge_post.x > standard_post.x:
                return False
        if position.located == "右":
            # print("you")
            if judge_post.x < standard_post.x:
                return False
        if position.located == "上":
            # print("上")
            if judge_post.y > standard_post.y:
                # print("返回false")
                return False
        if position.located == "下":
            # print("xia")
            if judge_post.y < standard_post.y:
                return False
    return True


def get_angle(angle1, angle2, angle3, angle4):
    """
    计算连个向量直接的夹角

    :param angle1:
    :param angle2:
    :param angle3:
    :param angle4:
    :return:
    """
    if (
        angle1.visibility <= 0.1
        or angle2.visibility <= 0.1
        or angle3.visibility <= 0.1
        or angle4.visibility <= 0.1
    ):
        return -1
    v1 = [angle1.x, angle1.y, angle2.x, angle2.y]
    v2 = [angle3.x, angle3.y, angle4.x, angle4.y]
    dx1 = v1[2] - v1[0]
    dy1 = v1[3] - v1[1]
    dx2 = v2[2] - v2[0]
    dy2 = v2[3] - v2[1]
    angle1 = math.atan2(dy1, dx1)
    angle1 = int(angle1 * 180 / math.pi)
    # print(angle1)
    angle2 = math.atan2(dy2, dx2)
    angle2 = int(angle2 * 180 / math.pi)
    # print(angle2)

    included_angle = (
        abs(angle1 - angle2) if (angle1 * angle2 >= 0) else (abs(angle1) + abs(angle2))
    )

    if included_angle > 180:
        included_angle = 360 - included_angle
    return included_angle

lock = threading.Lock()
result_post: Optional = None
game = None
input_lock = False
close = False


class PlayService:
    def __init__(self):
        self.mpPose = mp.solutions.pose
        self.draw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=True,
            smooth_segmentation=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.judge_action = False
        self.actions = None

    @staticmethod
    def inputKey() -> None:
        global input_lock
        while True:
            if close:
                break
            if input_lock:
                input_lock = False
                if result_post is not None:
                    game.actions.sort(key=lambda x: x.level)
                    for action in game.actions:
                        judge_action = True
                        angles = action.judge.angles
                        for angle in angles:
                            angle_result = judgeAngles(angle, result_post)
                            if angle_result is False:
                                judge_action = False
                                break
                        positions = action.judge.positions
                        for position in positions:
                            position_result = judgePosition(position, result_post)
                            if position_result is False:
                                judge_action = False
                                break
                        input_keys = action.keys.split("+")
                        if judge_action:
                            for key in input_keys:
                                if action.keys in ("a", "d", "left", "right"):
                                    pyautogui.keyDown(key)
                                    time.sleep(0.1)
                                    pyautogui.keyUp(key)
                                else:
                                    pyautogui.hotkey(key)
                time.sleep(0.1)

    @staticmethod
    def readGame():
        return None
        # 最核心的方法，用于读取动作检测动作是否符合要求，并执行对应的操作

    def playGame(self, new_game) -> None:
        cap = cv2.VideoCapture(0)
        play = PlayService()
        pTime = 0
        t = threading.Thread(target=self.inputKey)
        t.start()
        global game
        global result_post
        global input_lock
        game = new_game
        while cap.isOpened():
            ret, frame = cap.read()
            read_result = play.readImage(ret, frame)
            input_lock = True
            result_image = read_result["image"]
            if read_result["pose"] is not None:
                result_post = read_result["pose"]
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            show_result_image = result_image.copy()
            cv2.putText(
                show_result_image,
                "fps:" + str(int(fps)),
                (100, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (255, 0, 255),
                3,
            )
            cv2.imshow("action", show_result_image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                global close
                close = True
                break

    def readImage(self, ret, frame) -> dict:
        """
        读取对应的图片，返回对应数组 （只有动作数组 和 图片）

        :param ret:
        :param frame:
        :return:
        """
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = self.pose.process(image)

            # image.flags.writeable = True
            if results.pose_landmarks:
                # 这个还需要乘以对应的宽高
                self.draw.draw_landmarks(
                    image, results.pose_landmarks, self.mpPose.POSE_CONNECTIONS
                )
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            image = np.fliplr(image)
            return {"pose": results.pose_landmarks, "image": image}
        return None


# 新的方案，让用户进行关键点的设置。
# 判断条件，角度，位置，距离（暂定）。
# 角度：需要选择4个点的位置，然后计算出角度，然后判断是否符合条件。
# 位置：可以让多个点再某个点的相对位置（上下左右）。
# 与，或，非三种进行连接。理论上我就可以实现对绝大部分的动作进行检测设置。
if __name__ == "__main__":
    pass
    # 步骤一读取摄像头
    # cap = cv2.VideoCapture(0)
    # play = PlayService()
    # # 先读取标准的动作库里面的动作
    # standard_result = play.readAction()
    # game = Game()
    # play.playGame(game)
    # 开始读取摄像头并且返回对应的姿势的数组和图片。
    # 步骤二 读取动作库
    # 步骤三 开始游戏
    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     read_result = play.readImage(ret, frame)
    #     result_image = read_result["image"]
    #     result_post = read_result["pose"]
    #     play.playGame(game, result_post)
