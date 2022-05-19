from entity.judge import Judge


class Action:
    def __init__(self, name: str, level: str, type: str, judge: Judge, keys: str):
        # 动作名称
        self.name = name
        # 优先级
        self.level = level
        # 动作类型 自定义 或者我这边预先设置好的
        self.type = type
        # 动作判断条件
        self.judge = judge
        # 对应的按键招收
        self.keys = keys
