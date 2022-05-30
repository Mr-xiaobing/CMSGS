import os

import jsonpickle
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QDialog, QPushButton, QWidget, QLabel, QScrollArea

from gui.AddGameUi import AddGameUi
from service.PlayService import PlayService
from service.PlayShootingGameService import PlayShootingGameService


class LocalActionLibraryUi(QDialog):

    def __init__(self):
        super().__init__()
        self.back_home_button = None
        self.setupUi()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def action_ui(self, actions, game, index, index_y):
        action_ui = QWidget(actions)
        action_ui.resize(200, 300)
        action_ui.move((200*index)+(15*index), 320*index_y)
        game_name = QLabel(action_ui)
        game_name.setText("游戏名称："+game.name)
        object_name = "game"+str(index)
        action_ui.setObjectName(object_name)
        action_ui.setStyleSheet("#"+object_name+"{border:1px solid}")
        game_name.move(10, 20)

        description_label = QLabel(action_ui)
        description_label.setMaximumSize(200, 170)
        description_label.setText("介绍：\n"+game.description)
        description_label.move(10, 50)
        description_label.setWordWrap(True)

        play_game_button = QPushButton(action_ui)
        play_game_button.setText("开始游戏")
        play_game_button.setMinimumSize(200, 30)
        play_game_button.move(0, 240)
        play_game_button.clicked.connect(lambda: self.play_local_game(game))

        edit_button = QPushButton(action_ui)
        edit_button.setText("修改动作")
        edit_button.setMinimumSize(200, 30)
        edit_button.move(0, 270)
        edit_button.clicked.connect(lambda: self.edit_game(game))

    def shooting(self):
        shootingGame = PlayShootingGameService()
        shootingGame.play()

    def edit_game(self, game):
        add_game_ui = AddGameUi(game)
        add_game_ui.show()

    def play_local_game(self, game):
        play = PlayService()
        play.playGame(game)

    def back_home_ui(self):
        self.close()

    def setupUi(self):
        self.resize(1500, 1000)
        self.setWindowTitle("我的动作库")
        self.center()
        self.back_home_button = QPushButton(self)
        self.back_home_button.setText("返回主页")
        self.back_home_button.move(120, 60)
        self.back_home_button.setMinimumSize(200, 80)

        title = QLabel(self)
        title.setText("本地动作仓库")
        title.setStyleSheet("font-size:40px;color:#45D4FF;font-weight:bold")
        title.move(640, 100)

        all_action_button = QPushButton(self)
        all_action_button.setText("全部动作")
        all_action_button.move(120, 180)
        all_action_button.setMinimumSize(120, 50)

        shooting_action_button = QPushButton(self)
        shooting_action_button.setText("射击模式")
        shooting_action_button.move(250, 180)
        shooting_action_button.setMinimumSize(120, 50)
        shooting_action_button.clicked.connect(lambda: self.shooting())
        pk_action_button = QPushButton(self)
        pk_action_button.setText("暂定")
        pk_action_button.move(380, 180)
        pk_action_button.setMinimumSize(120, 50)

        pk_action_button = QPushButton(self)
        pk_action_button.setText("其他")
        pk_action_button.move(510, 180)
        pk_action_button.setMinimumSize(120, 50)

        actions = QWidget(self)
        actions.setMinimumSize(1300, 2000)
        actions.move(120, 250)
        actions.setObjectName("game_actions")
        actions.setStyleSheet("#game_actions{border:1px solid}")

        scroll_area = QScrollArea(self)
        scroll_area.setWidget(actions)
        scroll_area.move(120, 250)
        scroll_area.setMinimumSize(1320, 700)
        prefix_url = "./data/"
        files = os.listdir(prefix_url)
        index = 0
        index_y = -1
        for game_str in files:
            if index % 6 == 0:
                index_y = index_y+1
                index = 0
            with open(prefix_url+game_str, encoding="utf-8") as game_file:
                # dict_game =
                s = game_file.read()
                game = jsonpickle.decode(s)
                self.action_ui(actions, game, index, index_y)
                index = index + 1
