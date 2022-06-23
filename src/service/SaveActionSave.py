class ActionService:
    def __init__(self, action_dao):
        self.action_dao = action_dao

    #  录入保存动作
    @staticmethod
    def save(action):
        # （ 存入的对应的图片（本地路径） data里面 ）
        # （ 存对应的数组 ）
        # （ 存名称 ）
        return action.save()

    #  读取动作
    @staticmethod
    def read(action):
        return action.read()

    # 更新动作
    @staticmethod
    def update(action):
        return action.update()

    # 删除动作
    @staticmethod
    def delete(action):
        return action.delete()

    # 查看所有动作
    def getAllAction(self):
        return self.action_dao.getAllAction()
