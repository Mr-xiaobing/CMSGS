
class ActionService:

    def __init__(self, action_dao):
        self.action_dao = action_dao

    #  录入保存动作
    def save(self, action):
        # （ 存入的对应的图片（本地路径） data里面 ）
        # （ 存对应的数组 ）
        # （ 存名称 ）
        return action.save()
    #  读取动作
    def read(self, action):
        return action.read()

    # 更新动作
    def update(self, action):
        return action.update()

    # 删除动作
    def delete(self, action):
        return action.delete()

    # 查看所有动作
    def getAllAction(self):
        return self.action_dao.getAllAction()