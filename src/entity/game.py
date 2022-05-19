from typing import List

from entity.action import Action


class Game:
    def __init__(self, name: str, image: str, type: str, description: str, actions: List[Action]):
        # Game name
        self.name = name
        # Game image
        self.image = image
        # Game Type
        self.type = type
        # Game description
        self.description = description
        # Game action list
        # 动作库主要包括：设置的按钮对应的动作，（名称，按键，数组）
        self.actions = actions
