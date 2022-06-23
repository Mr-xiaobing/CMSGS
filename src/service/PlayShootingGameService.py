import math
import sys
import time

import cv2
import mediapipe as mp
import numpy as np
import pyautogui
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
        abs(angle1 - angle2) if (angle1 * angle2 >= 0) else (abs(angle1) + abs(angle2))
    )

    if included_angle > 180:
        included_angle = 360 - included_angle
    return included_angle


class PlayShootingGameService:
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
        self.isShooting = True
        # app = QApplication(sys.argv)
        # desktop = QGuiApplication.primaryScreen().availableGeometry()
        # 屏幕的高
        self.height = 2160
        # # 屏幕宽
        self.width = 3840

    def readImage(self, ret, frame) -> dict:
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

    def shooting(self, position_list):
        # 判断是否符合点击条件 还是用角度来判断
        x1 = position_list["left_position"][4][1]
        y1 = position_list["left_position"][4][2]
        x2 = position_list["left_position"][3][1]
        y2 = position_list["left_position"][3][2]
        x3 = position_list["left_position"][2][1]
        y3 = position_list["left_position"][2][2]
        angle = getAngle(x2, y2, x1, y1, x2, y2, x3, y3)
        if 150 < angle < 180:
            self.isShooting = True

        if 0 < angle < 150 and self.isShooting:
            pyautogui.click()
            self.isShooting = False

    def findPosition(self, results, img, draw=True):
        left_list = []
        right_list = []
        index = 0
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                print(results.multi_handedness)
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    # 展示视频上的位置
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # 具体鼠标移动到的位置
                    mx, my = int(lm.x * self.width), int(lm.y * self.height)

                    if index == 0:
                        left_list.append([id, cx, cy, mx, my])
                    else:
                        right_list.append([id, cx, cy, mx, my])

                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                index += 1
        return {"left_position": left_list, "right_position": right_list}

    def play(self):
        pyautogui.PAUSE = 0
        cap = cv2.VideoCapture(0)
        pTime = 0
        while cap.isOpened():
            ret, frame = cap.read()
            frame = np.fliplr(frame)
            read_result = self.readImage(ret, frame)
            result_image = read_result["image"]
            result_hands = read_result["hands"]
            position_list = self.findPosition(result_hands, result_image)
            if len(position_list["left_position"]) > 8:
                pyautogui.moveTo(
                    position_list["left_position"][8][3],
                    position_list["left_position"][8][4],
                )
                self.shooting(position_list)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            result_image = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)
            result_image = cv2.resize(result_image, (self.width, self.height))
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


if __name__ == "__main__":
    test = PlayShootingGameService()
    test.play()
