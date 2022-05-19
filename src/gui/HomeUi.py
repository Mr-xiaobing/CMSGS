import sys

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication

from entity.game import Game
from gui.AddGameUi import AddGameUi
from gui.LocalActionLibraryUi import LocalActionLibraryUi


class HomeUi(QWidget):
    def __init__(self):
        super().__init__()
        self.action_library_button = None
        self.add_game_button = None
        self.setupUi()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def click_add_game(self):
        game = Game("", "", "", "", [])
        self.add_game_ui = AddGameUi(game)
        # add_game_ui.show()

    def click_local_action_library(self):
        self.local_action_library_ui = LocalActionLibraryUi()

    def setupUi(self):
        self.resize(600, 400)
        self.setWindowTitle("主菜单")
        self.center()
        self.action_library_button = QPushButton(self)
        self.action_library_button.setText("我的动作仓库")
        self.action_library_button.move(100, 150)
        self.action_library_button.setMinimumSize(100, 40)

        self.add_game_button = QPushButton(self)
        self.add_game_button.setText("添加动作")
        self.add_game_button.move(250, 150)
        self.add_game_button.setMinimumSize(100, 40)

        add_game_button = QPushButton(self)
        add_game_button.setText("在线动作仓库(暂未开发）")
        add_game_button.move(400, 150)
        add_game_button.setMinimumSize(100, 40)

        self.show()
