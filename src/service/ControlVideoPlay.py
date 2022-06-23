import math
import sys
import time
import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from typing import Callable
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication

# 读取对应的图片，返回对应数组 （只有动作数组 和 图片）
from service.PlayService import get_angle


def getAngle(x1, y1, x2, y2, x3, y3, x4, y4):
    v1 = [x1, y1, x2, y2]
    v2 = [x3, y3, x4, y4]
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
        abs(angle1 - angle2) if angle1 * angle2 >= 0 else (abs(angle1) + abs(angle2))
    )

    if included_angle > 180:
        included_angle = 360 - included_angle
    return included_angle


class ControlVideoPlay:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.draw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.isControl = True
        self.count = 50

    def readImage(self, ret, frame) -> None | dict:
        """
        返回关键点 和 图像

        :param ret:
        :param frame:
        :return:
        """
        if ret:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.hands.process(image)
            # image.flags.writeable = True
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    # 这个还需要乘以对应的宽高
                    self.draw.draw_landmarks(
                        image, handLms, self.mpHands.HAND_CONNECTIONS
                    )
            return {"hands": results, "image": image}
        return None

    @staticmethod
    def stopAndPalyVideo(position) -> bool:
        """
        暂停/播放

        :param position:
        :return:
        """
        if position["right_position"]:
            x1 = position["right_position"][8][1]
            y1 = position["right_position"][8][2]
            x2 = position["right_position"][5][1]
            y2 = position["right_position"][5][2]
            x3 = position["right_position"][3][1]
            y3 = position["right_position"][3][2]
            x4 = position["right_position"][4][1]
            y4 = position["right_position"][4][2]
            angle = getAngle(x2, y2, x1, y1, x3, y3, x4, y4)

            vx1 = 0
            vy1 = 0
            vx2 = 0
            vy2 = 1
            vx3 = position["right_position"][12][1]
            vy3 = position["right_position"][12][2]
            vx4 = position["right_position"][9][1]
            vy4 = position["right_position"][9][2]
            v_angle = getAngle(vx1, vy1, vx2, vy2, vx3, vy3, vx4, vy4)
            if (
                70 < angle < 85
                and position["right_position"][20][2] < position["right_position"][4][2]
                and position["right_position"][16][2] < position["right_position"][4][2]
                and position["right_position"][12][2] < position["right_position"][4][2]
                and position["right_position"][8][2] < position["right_position"][4][2]
                and 0 <= v_angle <= 15
            ):
                print("播放/暂停")
                pyautogui.hotkey(" ")
                time.sleep(2.5)
                return True
        elif position["left_position"]:
            x1 = position["left_position"][8][1]
            y1 = position["left_position"][8][2]
            x2 = position["left_position"][5][1]
            y2 = position["left_position"][5][2]
            x3 = position["left_position"][3][1]
            y3 = position["left_position"][3][2]
            x4 = position["left_position"][4][1]
            y4 = position["left_position"][4][2]
            angle = getAngle(x2, y2, x1, y1, x3, y3, x4, y4)

            vx1 = 0
            vy1 = 0
            vx2 = 0
            vy2 = 1
            vx3 = position["left_position"][12][1]
            vy3 = position["left_position"][12][2]
            vx4 = position["left_position"][9][1]
            vy4 = position["left_position"][9][2]
            v_angle = getAngle(vx1, vy1, vx2, vy2, vx3, vy3, vx4, vy4)
            if (
                70 < angle < 85
                and position["left_position"][20][2] < position["left_position"][4][2]
                and position["left_position"][16][2] < position["left_position"][4][2]
                and position["left_position"][12][2] < position["left_position"][4][2]
                and position["left_position"][8][2] < position["left_position"][4][2]
                and 0 <= v_angle <= 10
            ):
                print("播放/暂停")
                pyautogui.hotkey(" ")
                time.sleep(2)
                return True
        return False

    @staticmethod
    def nextVideo(position) -> bool:
        """
        下一个视频

        :param position:
        :return:
        """
        if position["left_position"]:
            finger_pip6 = position["left_position"][6]
            finger_pip10 = position["left_position"][10]
            finger_pip14 = position["left_position"][14]
            finger_pip18 = position["left_position"][18]

            finger_tip8 = position["left_position"][8]
            finger_tip12 = position["left_position"][12]
            finger_tip16 = position["left_position"][16]
            finger_tip20 = position["left_position"][20]

            x1 = position["left_position"][8][1]
            y1 = position["left_position"][8][2]
            x2 = position["left_position"][5][1]
            y2 = position["left_position"][5][2]
            x3 = position["left_position"][1][1]
            y3 = position["left_position"][1][2]
            x4 = position["left_position"][4][1]
            y4 = position["left_position"][4][2]
            angle = getAngle(x2, y2, x1, y1, x3, y3, x4, y4)

            lx1 = 0
            ly1 = 0
            lx2 = 2
            ly2 = 0
            lx3 = position["left_position"][5][1]
            ly3 = position["left_position"][5][2]
            lx4 = position["left_position"][8][1]
            ly4 = position["left_position"][8][2]
            l_angle = getAngle(lx1, ly1, lx2, ly2, lx3, ly3, lx4, ly4)
            if (
                position["left_position"][18][1] > position["left_position"][4][1]
                and position["left_position"][14][1] > position["left_position"][4][1]
                and position["left_position"][10][1] > position["left_position"][4][1]
                and position["left_position"][6][1] > position["left_position"][4][1]
                and position["left_position"][4][2] < position["left_position"][8][2]
                and 70 < angle < 85
                and 0 <= l_angle <= 15
                and finger_pip6[1] < finger_tip8[1]
                and finger_pip10[1] < finger_tip12[1]
                and finger_pip14[1] < finger_tip16[1]
                and finger_pip18[1] < finger_tip20[1]
            ):
                print("下一个视频")
                pyautogui.hotkey("]")
                time.sleep(2.5)
                return True
        return False

    @staticmethod
    def lastVideo(position) -> bool:
        """
        上一个视频

        :param position:
        :return:
        """
        if position["right_position"]:
            finger_pip6 = position["right_position"][6]
            finger_pip10 = position["right_position"][10]
            finger_pip14 = position["right_position"][14]
            finger_pip18 = position["right_position"][18]

            finger_tip8 = position["right_position"][8]
            finger_tip12 = position["right_position"][12]
            finger_tip16 = position["right_position"][16]
            finger_tip20 = position["right_position"][20]

            x1 = position["right_position"][8][1]
            y1 = position["right_position"][8][2]
            x2 = position["right_position"][5][1]
            y2 = position["right_position"][5][2]
            x3 = position["right_position"][3][1]
            y3 = position["right_position"][3][2]
            x4 = position["right_position"][4][1]
            y4 = position["right_position"][4][2]
            angle = getAngle(x2, y2, x1, y1, x3, y3, x4, y4)

            lx1 = 0
            ly1 = 0
            lx2 = 2
            ly2 = 0
            lx3 = position["right_position"][5][1]
            ly3 = position["right_position"][5][2]
            lx4 = position["right_position"][8][1]
            ly4 = position["right_position"][8][2]
            l_angle = getAngle(lx2, ly2, lx1, ly1, lx3, ly3, lx4, ly4)
            if (
                position["right_position"][20][1] < position["right_position"][4][1]
                and position["right_position"][4][2] < position["right_position"][8][2]
                and 70 < angle < 85
                and 0 <= l_angle <= 10
                and finger_pip6[1] > finger_tip8[1]
                and finger_pip10[1] > finger_tip12[1]
                and finger_pip14[1] > finger_tip16[1]
                and finger_pip18[1] > finger_tip20[1]
            ):
                print("上一个视频")
                pyautogui.hotkey("[")
                time.sleep(2.5)
                return True
        return False

    @staticmethod
    def speedUp(position) -> bool:
        """
        快进

        :param position:
        :return:
        """
        if position["left_position"]:
            finger_pip6 = position["left_position"][6]
            finger_pip10 = position["left_position"][10]
            finger_pip14 = position["left_position"][14]
            finger_pip18 = position["left_position"][18]

            finger_tip8 = position["left_position"][8]
            finger_tip12 = position["left_position"][12]
            finger_tip16 = position["left_position"][16]
            finger_tip20 = position["left_position"][20]

            x1 = position["left_position"][8][1]
            y1 = position["left_position"][8][2]
            x2 = position["left_position"][5][1]
            y2 = position["left_position"][5][2]
            x3 = position["left_position"][3][1]
            y3 = position["left_position"][3][2]
            x4 = position["left_position"][4][1]
            y4 = position["left_position"][4][2]
            angle = getAngle(x2, y2, x1, y1, x3, y3, x4, y4)

            lx1 = 0
            ly1 = 0
            lx2 = 2
            ly2 = 0
            lx3 = position["left_position"][5][1]
            ly3 = position["left_position"][5][2]
            lx4 = position["left_position"][8][1]
            ly4 = position["left_position"][8][2]
            l_angle = getAngle(lx1, ly1, lx2, ly2, lx3, ly3, lx4, ly4)
            if (
                position["left_position"][18][1] > position["left_position"][4][1]
                and position["left_position"][14][1] > position["left_position"][4][1]
                and position["left_position"][10][1] > position["left_position"][4][1]
                and position["left_position"][6][1] > position["left_position"][4][1]
                and position["left_position"][4][2] < position["left_position"][8][2]
                and 70 < angle < 85
                and 0 <= l_angle <= 15
                and finger_pip6[1] < finger_tip8[1]
                and finger_pip10[1] > finger_tip12[1]
                and finger_pip14[1] > finger_tip16[1]
                and finger_pip18[1] > finger_tip20[1]
            ):
                print("快进")
                pyautogui.hotkey("right")
                time.sleep(0.7)
                return True
        return False

    @staticmethod
    def speedDown(position) -> bool:
        """
        快退

        :param position:
        :return:
        """
        if position["right_position"]:
            finger_pip6 = position["right_position"][6]
            finger_pip10 = position["right_position"][10]
            finger_pip14 = position["right_position"][14]
            finger_pip18 = position["right_position"][18]

            finger_tip8 = position["right_position"][8]
            finger_tip12 = position["right_position"][12]
            finger_tip16 = position["right_position"][16]
            finger_tip20 = position["right_position"][20]

            x1 = position["right_position"][8][1]
            y1 = position["right_position"][8][2]
            x2 = position["right_position"][5][1]
            y2 = position["right_position"][5][2]
            x3 = position["right_position"][1][1]
            y3 = position["right_position"][1][2]
            x4 = position["right_position"][4][1]
            y4 = position["right_position"][4][2]
            angle = getAngle(x2, y2, x1, y1, x3, y3, x4, y4)

            lx1 = 0
            ly1 = 0
            lx2 = 2
            ly2 = 0
            lx3 = position["right_position"][5][1]
            ly3 = position["right_position"][5][2]
            lx4 = position["right_position"][8][1]
            ly4 = position["right_position"][8][2]
            l_angle = getAngle(lx2, ly2, lx1, ly1, lx3, ly3, lx4, ly4)
            if (
                position["right_position"][20][1] < position["right_position"][4][1]
                and position["right_position"][4][2] < position["right_position"][8][2]
                and 70 < angle < 85
                and 0 <= l_angle <= 10
                and finger_pip6[1] > finger_tip8[1]
                and finger_pip10[1] < finger_tip12[1]
                and finger_pip14[1] < finger_tip16[1]
                and finger_pip18[1] < finger_tip20[1]
            ):
                print("快退")
                pyautogui.hotkey("left")
                time.sleep(0.7)
                return True
        return False

    @staticmethod
    def mute(position) -> bool:
        """
        静音/音量

        :param position:
        :return:
        """
        if position["left_position"] and position["right_position"]:
            left_index_tip = position["left_position"][8]
            left_index_mcp = position["left_position"][5]

            right_index_tip = position["right_position"][8]
            right_index_mcp = position["right_position"][5]
            angle = getAngle(
                left_index_mcp[1],
                left_index_mcp[2],
                left_index_tip[1],
                left_index_tip[2],
                right_index_mcp[1],
                right_index_mcp[2],
                right_index_tip[1],
                right_index_tip[2],
            )
            print("----")
            print(left_index_tip[1])
            print(right_index_tip[1])
            print(left_index_mcp[1])
            print(right_index_mcp[1])
            print("angle")
            print(angle)
            if (
                left_index_tip[1] > right_index_tip[1]
                and left_index_mcp[1] < right_index_mcp[1]
                and 60 < angle < 150
            ):
                print("静音")
                pyautogui.hotkey("m")
                time.sleep(2)
                return True
        return False

    @staticmethod
    def praise(position) -> bool:
        """
        点赞

        :param position:
        :return:
        """
        if position["right_position"]:
            right_finger_pip6 = position["right_position"][6]
            right_finger_pip10 = position["right_position"][10]
            right_finger_pip14 = position["right_position"][14]
            right_finger_pip19 = position["right_position"][19]

            right_finger_tip8 = position["right_position"][8]
            right_finger_tip12 = position["right_position"][12]
            right_finger_tip16 = position["right_position"][16]
            right_finger_tip20 = position["right_position"][20]

            right_thumb_ip = position["right_position"][3]
            right_thumb_tip = position["right_position"][4]
            right_thumb_cmc = position["right_position"][1]

            angle = getAngle(
                0,
                0,
                0,
                1,
                right_thumb_tip[1],
                right_thumb_tip[2],
                right_thumb_ip[1],
                right_thumb_ip[2],
            )
            if (
                right_finger_pip6[1] < right_thumb_cmc[1]
                and right_finger_pip10[1] < right_thumb_cmc[1]
                and right_finger_pip14[1] < right_thumb_cmc[1]
                and right_finger_pip19[1] < right_thumb_cmc[1]
                and right_finger_pip6[1] < right_finger_tip8[1]
                and right_finger_pip10[1] < right_finger_tip12[1]
                and right_finger_pip14[1] < right_finger_tip16[1]
                and right_finger_pip19[1] < right_finger_tip20[1]
                and right_thumb_tip[2] < right_finger_tip8[2]
                and right_thumb_tip[2] < right_thumb_ip[2] < right_thumb_cmc[2]
                and 0 < angle < 10
            ):
                print("点赞")
                pyautogui.hotkey("q")
                time.sleep(2)
                return True
        return False

    @staticmethod
    def threeEven(position) -> bool:
        """
        一键三连

        :param position:
        :return:
        """
        if position["right_position"] and position["left_position"]:
            judge_right = False
            right_finger_pip6 = position["right_position"][6]
            right_finger_pip10 = position["right_position"][10]
            right_finger_pip14 = position["right_position"][14]
            right_finger_pip19 = position["right_position"][19]

            right_finger_tip8 = position["right_position"][8]
            right_finger_tip12 = position["right_position"][12]
            right_finger_tip16 = position["right_position"][16]
            right_finger_tip20 = position["right_position"][20]

            right_thumb_ip = position["right_position"][3]
            right_thumb_tip = position["right_position"][4]
            right_thumb_cmc = position["right_position"][1]

            if (
                right_finger_pip6[1] < right_thumb_cmc[1]
                and right_finger_pip10[1] < right_thumb_cmc[1]
                and right_finger_pip14[1] < right_thumb_cmc[1]
                and right_finger_pip19[1] < right_thumb_cmc[1]
                and right_finger_pip6[1] < right_finger_tip8[1]
                and right_finger_pip10[1] < right_finger_tip12[1]
                and right_finger_pip14[1] < right_finger_tip16[1]
                and right_finger_pip19[1] < right_finger_tip20[1]
                and right_thumb_tip[2] < right_finger_tip8[2]
                and right_thumb_tip[2] < right_thumb_ip[2] < right_thumb_cmc[2]
            ):
                judge_right = True
            if judge_right:
                left_finger_pip6 = position["left_position"][6]
                left_finger_pip10 = position["left_position"][10]
                left_finger_pip14 = position["left_position"][14]
                left_finger_pip19 = position["left_position"][19]

                left_finger_tip8 = position["left_position"][8]
                left_finger_tip12 = position["left_position"][12]
                left_finger_tip16 = position["left_position"][16]
                left_finger_tip20 = position["left_position"][20]

                left_thumb_ip = position["left_position"][3]
                left_thumb_tip = position["left_position"][4]
                left_thumb_cmc = position["left_position"][1]

                if (
                    left_finger_pip6[1] > left_thumb_cmc[1]
                    and left_finger_pip10[1] > left_thumb_cmc[1]
                    and left_finger_pip14[1] > left_thumb_cmc[1]
                    and left_finger_pip19[1] > left_thumb_cmc[1]
                    and left_finger_pip6[1] > left_finger_tip8[1]
                    and left_finger_pip10[1] > left_finger_tip12[1]
                    and left_finger_pip14[1] > left_finger_tip16[1]
                    and left_finger_pip19[1] > left_finger_tip20[1]
                    and left_thumb_ip[2] < left_finger_tip8[2]
                    and left_thumb_tip[2] < left_thumb_ip[2] < left_thumb_cmc[2]
                ):
                    print("一键三连")
                    pyautogui.keyDown("q")
                    time.sleep(3)
                    pyautogui.keyUp("q")
                    return True
        return False

    @staticmethod
    def FullScreen(position) -> bool:
        """
        全屏

        :param position:
        :return:
        """
        if position["right_position"]:
            # right_thumb_cmc = position["right_position"][1]
            right_thumb_mcp = position["right_position"][2]
            right_finger_pip6 = position["right_position"][6]
            right_finger_pip10 = position["right_position"][10]
            right_finger_pip14 = position["right_position"][14]
            right_finger_pip18 = position["right_position"][18]

            right_thumb_tip = position["right_position"][4]
            right_finger_tip8 = position["right_position"][8]
            right_finger_tip12 = position["right_position"][12]
            right_finger_tip16 = position["right_position"][16]
            right_finger_tip20 = position["right_position"][20]

            angle = getAngle(
                0,
                0,
                0,
                1,
                right_thumb_tip[1],
                right_thumb_tip[2],
                right_thumb_mcp[1],
                right_thumb_mcp[2],
            )
            if (
                right_finger_pip6[2] < right_finger_tip8[2]
                and right_finger_pip10[2] < right_finger_tip12[2]
                and right_finger_pip14[2] < right_finger_tip16[2]
                and right_thumb_tip[2] < right_thumb_mcp[2]
                and right_finger_tip20[2] < right_finger_pip18[2]
                and 20 < angle < 50
            ):
                pyautogui.hotkey("f")
                print("全屏")
                time.sleep(2)
                return False
        return True

    def setControl(self, position) -> None:
        """
        取消控制

        :param position:
        :return:
        """
        if position["left_position"] and position["right_position"]:

            # right_thumb_tip = position["right_position"][4]
            # right_finger_tip8 = position["right_position"][8]
            # right_finger_tip12 = position["right_position"][12]
            # right_finger_tip16 = position["right_position"][16]
            # right_finger_tip20 = position["right_position"][20]

            left_wrist = position["left_position"][0]
            right_wrist = position["right_position"][0]

            if (left_wrist[1] - right_wrist[1]) > 0.1:
                if self.isControl:
                    self.count -= 1
                    if self.count < 0:
                        self.isControl = False
                        print("取消控制")
                        time.sleep(3)
                else:
                    if self.count > 100:
                        self.isControl = True
                        print("允许控制")
                        time.sleep(3)

    @staticmethod
    def findPosition(results) -> dict:
        left_list = []
        right_list = []
        index = 0
        if results.multi_hand_landmarks:
            # print(results.multi_handedness)
            for handLms in results.multi_hand_landmarks:
                if (
                    len(results.multi_handedness) == 1
                    and results.multi_handedness[0].classification[0].label == "Right"
                    and results.multi_handedness[0].classification[0].score > 0.95
                ):
                    for id, lm in enumerate(handLms.landmark):
                        right_list.append([id, lm.x, lm.y])
                elif (
                    len(results.multi_handedness) == 1
                    and results.multi_handedness[0].classification[0].label == "Left"
                    and results.multi_handedness[0].classification[0].score > 0.95
                ):
                    for id, lm in enumerate(handLms.landmark):
                        left_list.append([id, lm.x, lm.y])
                elif len(results.multi_handedness) == 2:
                    if index == 0:
                        for id, lm in enumerate(handLms.landmark):
                            right_list.append([id, lm.x, lm.y])
                    else:
                        for id, lm in enumerate(handLms.landmark):
                            left_list.append([id, lm.x, lm.y])
                index += 1
        return {"left_position": left_list, "right_position": right_list}

    def play(self):
        cap = cv2.VideoCapture(0)
        pTime = 0
        while cap.isOpened():
            ret, frame = cap.read()
            frame = np.fliplr(frame)
            read_result: dict = self.readImage(ret, frame)
            result_image = read_result["image"]
            result_hands = read_result["hands"]
            position_list = self.findPosition(result_hands)

            # self.setControl(position_list)
            # 切换鼠标控制
            if self.isControl:
                fun_list: tuple[Callable, ...] = (
                    self.nextVideo,
                    self.lastVideo,
                    self.stopAndPalyVideo,
                    self.threeEven,
                    self.speedUp,
                    self.speedDown,
                    self.praise,
                    self.mute,
                    self.FullScreen,
                )
                for fun in fun_list:
                    if fun(position_list):  # 函数成功执行返回True，然后不执行后面的
                        break

            # todo 判断需要执行哪个手势
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            result_image = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)
            result_image = result_image.copy()
            cv2.putText(
                result_image,
                "fps:" + str(int(fps)),
                (100, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                3,
                (255, 0, 255),
                3,
            )
            cv2.imshow("action", result_image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
