from entity.game import Game
from gui.AddGameUi import AddGameUi
from gui.HomeUi import HomeUi
from gui.LocalActionLibraryUi import LocalActionLibraryUi


class Controller:
    def __init__(self):
        self.home = HomeUi()
        game = Game("", "", "动作游戏", "", [])
        self.addGame = AddGameUi(game)
        self.localActionLibraryUi = LocalActionLibraryUi()
        self.setup()

    def addGame_to_home(self):
        self.addGame.save_game()
        self.home.show()

    def localAction_to_home(self):
        self.localActionLibraryUi.close()
        self.home.show()

    def home_to_library(self):
        self.home.close()
        self.localActionLibraryUi = LocalActionLibraryUi()
        self.localActionLibraryUi.back_home_button.clicked.connect(
            self.localAction_to_home
        )
        self.localActionLibraryUi.show()

    def home_to_addGame(self):
        self.home.close()
        game = Game("", "", "动作游戏", "", [])
        self.addGame = AddGameUi(game)
        self.addGame.save_button.clicked.connect(self.addGame_to_home)
        self.addGame.back_button.clicked.connect(self.addGame_to_home_back)
        self.addGame.show()

    def addGame_to_home_back(self):
        self.addGame.close()
        self.home.show()

    def setup(self):
        self.home.action_library_button.clicked.connect(self.home_to_library)
        self.home.add_game_button.clicked.connect(self.home_to_addGame)
        self.addGame.save_button.clicked.connect(self.addGame_to_home)
        self.localActionLibraryUi.back_home_button.clicked.connect(
            self.localAction_to_home
        )
        self.addGame.back_button.clicked.connect(self.addGame_to_home_back)
        self.home.show()
