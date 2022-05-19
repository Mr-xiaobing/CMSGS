class Position:
    def __init__(self, description: str, judge_point: str, standard: str, located: str):
        self.description = description
        # 数组 例如 [1,2,3]
        self.judge_point = judge_point
        # 整数 例如 1
        self.standard = standard
        # 字符串 表示位置 例如 'left' 表示left里面的点再standard点的左边 0表示左 1表示右 2表示上 3表示下
        self.located = located
