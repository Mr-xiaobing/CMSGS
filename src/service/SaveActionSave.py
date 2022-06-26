class ActionService:
    def __init__(self, action_dao):
        self.action_dao = action_dao

    @staticmethod
    def save(action):
        """
        录入保存动作

        :param action:
        :return:
        """
        # （ 存入的对应的图片（本地路径） data里面 ）
        # （ 存对应的数组 ）
        # （ 存名称 ）
        return action.save()

    @staticmethod
    def read(action):
        """
        读取动作

        :param action:
        :return:
        """
        return action.read()

    @staticmethod
    def update(action):
        """
        更新动作

        :param action:
        :return:
        """
        return action.update()

    @staticmethod
    def delete(action):
        """
        删除动作

        :param action:
        :return:
        """
        return action.delete()

    def getAllAction(self):
        """
        查看所有动作

        :return:
        """
        return self.action_dao.getAllAction()
