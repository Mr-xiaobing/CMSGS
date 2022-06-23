class Angle:
    def __init__(
        self,
        description: str,
        organ1: str,
        organ2: str,
        organ3: str,
        organ4: str,
        angle1: str,
        angle2: str,
    ):
        self.description = description
        # 1 2 两个点组成一个直线
        self.organ1 = organ1
        self.organ2 = organ2
        # 3 4 两个点组成一个直线
        self.organ3 = organ3
        self.organ4 = organ4
        # 在角度 1，2 之间
        self.angle1 = angle1
        self.angle2 = angle2
