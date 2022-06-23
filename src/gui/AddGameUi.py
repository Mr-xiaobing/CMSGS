import json
import sys

import jsonpickle
from PyQt6 import sip
from PyQt6.QtGui import QGuiApplication, QPixmap, QIntValidator
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QTableWidget, \
    QHeaderView, QPushButton, QTableWidgetItem, QVBoxLayout, QScrollArea, QDialog

# 让窗口居中

from entity.action import Action
from entity.angle import Angle
from entity.game import Game
from entity.judge import Judge
from entity.position import Position

def action_update_name(input_action, save_action):
    save_action.name = input_action.text()


def action_update_level(input_action, save_action):
    save_action.level = input_action.text()


def action_update_keys(input_action, save_action):
    save_action.keys = input_action.text()


class AddGameUi(QDialog):
    def __init__(self, game):
        super().__init__()
        self.save_button = None
        self.back_button = None
        self.game = game
        self.r_main = None
        self.setupUi()

    def setupUi(self):
        self.resize(1500, 1000)
        self.center()
        self.setWindowTitle("创建游戏")
        # 游戏名称
        game_name_label = QLabel(self)
        game_name_label.setText("游戏名称:")
        game_name_input = QLineEdit(self)
        game_name_label.move(50, 50)
        game_name_input.setPlaceholderText("不要和已有的重复")
        game_name_input.move(110, 48)
        game_name_input.setText(self.game.name)
        game_name_input.textChanged.connect(lambda: self.set_game_name(self.game, game_name_input))

        # 游戏介绍
        game_describe_label = QLabel(self)
        game_describe_edit = QTextEdit(self)
        game_describe_label.move(50, 90)
        game_describe_edit.move(110, 90)
        game_describe_label.setText("游戏描述:")
        game_describe_edit.setPlaceholderText("游戏的简单介绍，网页游戏请填写URL地址。")
        game_describe_edit.setText(self.game.description)
        game_describe_edit.textChanged.connect(lambda: self.set_game_description(self.game, game_describe_edit))

        # 游戏类型
        game_class_label = QLabel(self)
        game_class_box = QComboBox(self)
        game_class = ["动作游戏", "其他"]
        game_class_box.addItems(game_class)
        game_class_box.currentTextChanged.connect(lambda: self.set_game_type(self.game, game_class_box))
        game_class_label.move(50, 310)
        game_class_box.move(110, 308)
        game_class_label.setText("游戏类型:")
        # 动作表格
        game_table = QTableWidget(self)
        game_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        game_table.setRowCount(0)
        game_table.setColumnCount(5)
        game_table.setGeometry(50, 340, 650, 300)
        game_table.setHorizontalHeaderLabels(['动作名称', '动作类型', '动作优先级', '判断条件', '输出按键'])
        for i in range(len(self.game.actions)):
            self.show_actions(game_table, self.game.actions[i])
        game_table_add_item = QPushButton("add_item", self)
        game_table_add_item.setText("添加动作")
        game_table_add_item.move(320, 650)
        game_table_add_item.clicked.connect(lambda: self.add_action(game_table))
        # 关节点图片 帮助大家创建游戏
        game_post_image = QLabel(self)
        game_post_image.move(50, 500)
        game_post_image.setGeometry(50, 700, 650, 300)
        game_post_image.setPixmap(QPixmap("image/position.png"))
        game_post_image.setScaledContents(True)

        # 右边部分
        right_w = QWidget(self)
        right_w.resize(500, 1100)
        right_w.move(700, 50)
        judge_label = QLabel(right_w)
        judge_label.setText("判定条件")
        judge_label.setStyleSheet("font:bold 30px")
        judge_label.move(250, 0)

        self.save_button = QPushButton(self)
        self.save_button.setText("完成")
        self.save_button.resize(100, 60)
        self.save_button.move(600, 30)
        self.save_button.clicked.connect(lambda: self.save_game())

        self.back_button = QPushButton(self)
        self.back_button.setText("返回")
        self.back_button.resize(100, 60)
        self.back_button.move(750, 30)
        self.back_button.clicked.connect(lambda: self.close())
        # 动作部分

    def save_game(self):
        with open("./data/"+self.game.name+".json", "w", encoding="utf-8") as out_file:
            s = json.dumps(json.loads(jsonpickle.encode(self.game)), indent=4, ensure_ascii=False)
            out_file.write(s)
            # json.dump(self.game, out_file, default=lambda o: o.__dict__, ensure_ascii=False)
            # print(type(my_game))
            # d = json.loads(my_game)
            # new_game1 = DefaultMunch.fromDict(d)
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 添加动作判定
    def append_angle(self, action, lay):
        self.delete_all_children(lay)
        angle = Angle("", "", "", "", "", "", "")
        action.judge.angles.append(angle)
        self.show_judge(action, lay)

    # 添加位置判断
    def append_position(self, action, lay):
        self.delete_all_children(lay)
        position = Position("", "", "", "")
        action.judge.positions.append(position)
        self.show_judge(action, lay)

    def show_judge(self, action, lay):
        angle_index = 0
        for position in action.judge.positions:
            self.position_widget(position, lay, angle_index, action)
            angle_index = angle_index + 1
        for angle in action.judge.angles:
            self.angle_widget(angle, lay, angle_index, action)
            angle_index = angle_index + 1

    # 删除角度判定
    def delete_judge_angle(self, angle, action):
        action.judge.angles.remove(angle)
        self.edit_judge(action)

    # 删除位置判定
    def delete_judge_position(self, position, action):
        action.judge.positions.remove(position)
        self.edit_judge(action)

    # 角度判定的页面
    def angle_widget(self, angle, lay, index, action):
        action_angle = QWidget(lay)
        object_name = "position" + str(index)
        action_angle.setObjectName(object_name)
        action_angle.setStyleSheet("#" + object_name + "{border:1px solid}")
        action_angle.setMinimumSize(700, 200)
        action_angle.setMaximumSize(700, 200)
        action_angle.move(0, 210*index+40)
        vector_label_1 = QLabel(action_angle)
        vector_label_1.setText("向量1 :")
        vector_label_1.move(10, 30)

        vector_point_box_1 = QLineEdit(action_angle)
        vector_point_box_1.setText(angle.organ1)
        vector_point_box_1.setPlaceholderText("填图片上关节点的数字")
        vector_point_box_1.setMaximumWidth(150)
        vector_point_box_1.textChanged.connect(lambda: self.set_organ1_value(angle, vector_point_box_1))
        vector_point_box_1.move(60, 30)

        vector_point_box_2 = QLineEdit(action_angle)
        vector_point_box_2.setText(angle.organ2)
        vector_point_box_2.setPlaceholderText("填图片上关节点的数字")
        vector_point_box_2.setMaximumWidth(150)
        vector_point_box_2.textChanged.connect(lambda: self.set_organ2_value(angle, vector_point_box_2))
        vector_point_box_2.move(200, 30)

        vector_label_2 = QLabel(action_angle)
        vector_label_2.setText("向量2 :")
        vector_label_2.move(350, 30)

        vector_point_box_3 = QLineEdit(action_angle)
        vector_point_box_3.setMaximumWidth(150)
        vector_point_box_3.setPlaceholderText("填图片上关节点的数字")
        vector_point_box_3.setText(angle.organ3)
        vector_point_box_3.textChanged.connect(lambda: self.set_organ3_value(angle, vector_point_box_3))
        vector_point_box_3.move(400, 30)

        vector_point_box_4 = QLineEdit(action_angle)
        vector_point_box_4.setText(angle.organ4)
        vector_point_box_4.setPlaceholderText("填图片上关节点的数字")
        vector_point_box_4.setMaximumWidth(150)
        vector_point_box_4.textChanged.connect(lambda: self.set_organ4_value(angle, vector_point_box_4))
        vector_point_box_4.move(560, 30)

        angle_label = QLabel(action_angle)
        angle_label.move(10, 65)
        angle_label.setText("向量组成夹角范围 :")

        min_angle = QLineEdit(action_angle)
        min_angle.move(130, 65)
        min_angle.setValidator(QIntValidator(0, 180))
        min_angle.setPlaceholderText("例如:10")
        min_angle.setText(angle.angle1)
        min_angle.setMaximumWidth(80)
        min_angle.textChanged.connect(lambda: self.set_angle1_value(angle, min_angle))

        max_angle = QLineEdit(action_angle)
        max_angle.move(240, 65)
        max_angle.setValidator(QIntValidator(0, 180))
        max_angle.setPlaceholderText("例如:100")
        max_angle.setText(angle.angle2)
        max_angle.setMaximumWidth(80)
        max_angle.textChanged.connect(lambda: self.set_angle2_value(angle, max_angle))
        instructions = QLabel(action_angle)
        instructions.setText("说明:左边输入框为小的值，右边输入框为大的值."+"\n"+"如果向量1与向量2组成的夹角的角度在这个范围之内，"+"\n"+"则判断为成功做出动作")
        instructions.move(400, 65)

        description_label = QLabel(action_angle)
        description_label.setText("说明 :")
        description_label.move(10, 100)
        description = QLineEdit(action_angle)
        description.move(60, 100)
        description.setMinimumWidth(300)
        description.setText(angle.description)
        description.textChanged.connect(lambda: self.set_description_value(angle, description))

        delete_angle = QPushButton(action_angle)
        delete_angle.setText("删除")
        delete_angle.move(260, 130)
        delete_angle.clicked.connect(lambda: self.delete_judge_angle(angle, action))

        action_angle.show()

    # 位置判定的页面
    def position_widget(self, position, lay, index, action):
        action_position = QWidget(lay)
        object_name = "position"+str(index)
        action_position.setObjectName(object_name)
        action_position.setStyleSheet("#"+object_name+"{border:1px solid}")
        action_position.setMinimumSize(700, 200)
        action_position.setMinimumSize(700, 200)
        action_position.move(0, 210*index+40)
        judge_point_label = QLabel(action_position)
        judge_point_label.setText("判断点:")
        judge_point_label.move(10, 30)
        judge_point_input = QLineEdit(action_position)
        judge_point_input.setText(position.judge_point)
        judge_point_input.setPlaceholderText("填图片上对应的关节点数字")
        judge_point_input.setMinimumWidth(200)
        judge_point_input.textChanged.connect(lambda: self.set_judge_point(position, judge_point_input))
        judge_point_input.move(60, 30)

        judge_point_description = QLabel(action_position)
        judge_point_description.setText("说明:填写关节点的数字，多个使用竖线分隔。\n例如:10|18|19")
        judge_point_description.move(320, 30)

        standard_point_label = QLabel(action_position)
        standard_point_label.setText("标准点:")
        standard_point_label.move(10, 65)
        standard_point_input = QLineEdit(action_position)
        standard_point_input.setText(position.standard)
        standard_point_input.setPlaceholderText("只能填写一个关节点数字")
        standard_point_input.setMinimumWidth(200)
        standard_point_input.move(60, 65)
        standard_point_input.textChanged.connect(lambda: self.set_standard_point(position, standard_point_input))

        judge_in_standard_label = QLabel(action_position)
        judge_in_standard_label.setText("判断点位于标准点的:")
        judge_in_standard_label.move(10, 100)
        judge_in_standard_input = QLineEdit(action_position)
        judge_in_standard_input.setText(position.located)
        judge_in_standard_input.setMaximumWidth(80)
        judge_in_standard_input.move(130, 98)
        judge_in_standard_input.textChanged.connect(lambda: self.set_located_point(position, judge_in_standard_input))

        judge_in_standard_description = QLabel(action_position)
        judge_in_standard_description.move(250, 100)
        judge_in_standard_description.setText("只能填写：上，下，左，右。\n例如：填写上表示判断点位于标准的上边，则判断动作为成功")

        position_description_label = QLabel(action_position)
        position_description_label.setText("说明:")
        position_description_label.move(10, 135)

        position_description_input = QLineEdit(action_position)
        position_description_input.setText(position.description)
        position_description_input.setMinimumWidth(300)
        position_description_input.move(60, 135)
        position_description_input.textChanged.connect(lambda: self.set_position_description_value(position, position_description_input))

        delete_position = QPushButton(action_position)
        delete_position.setText("删除")
        delete_position.move(260, 165)
        delete_position.clicked.connect(lambda: self.delete_judge_position(position, action))

        action_position.show()

    def delete_all_children(self, lay):
        for i in lay.children():
            if not i.objectName() == "box_layout":
                i.deleteLater()
                sip.delete(i)

    # 侧边任务的编辑
    def edit_judge(self, action):
        if not self.r_main == None:
            self.r_main.close()
            self.r_main.deleteLater()
            sip.delete(self.r_main)
            for i in self.children():
                print(i)
        self.r_main = QWidget(self)
        self.r_main.resize(730, 1000)
        self.r_main.move(700, 30)

        r_action_name = QLabel(self.r_main)
        r_action_name.setText("动作名称:"+str(action.name))
        r_action_name.move(450, 40)
        r_main_action = QWidget(self.r_main)
        r_main_action.move(20, 110)
        r_main_action.setMinimumSize(700, 20000)
        r_main_action.setMaximumSize(700, 200000)
        r_main_action.setObjectName("r_main_action")
        r_main_action.setStyleSheet("#r_main_action{border:1px solid}")
        lay = QVBoxLayout()
        lay.setObjectName("box_layout")
        scrollArea = QScrollArea(self.r_main)
        scrollArea.move(20, 110)
        scrollArea.setMinimumWidth(720)
        scrollArea.setMinimumHeight(800)
        scrollArea.setWidget(r_main_action)
        scrollArea.show()
        r_main_action.setLayout(lay)
        r_main_add_button = QWidget(self.r_main)
        r_main_add_button.move(0, 10)
        add_action_position_button = QPushButton(r_main_add_button)
        add_action_position_button.move(220, 60)
        add_action_position_button.setText("添加位置判定")
        add_action_position_button.clicked.connect(lambda: self.append_position(action, scrollArea.widget()))
        add_action_angle_button = QPushButton(r_main_add_button)
        add_action_angle_button.move(330, 60)
        add_action_angle_button.setText("添加角度判定")
        add_action_angle_button.clicked.connect(lambda: self.append_angle(action, scrollArea.widget()))
        self.show_judge(action, scrollArea.widget())
        self.r_main.show()

    def add_action(self, table):
        index = table.rowCount()
        table.insertRow(index)
        judge_button = QPushButton()
        judge_button.setText("编辑")
        judge = Judge()
        action = Action("", "", "", judge, "")
        self.game.actions.append(action)

        action_name = QLineEdit()
        table.setCellWidget(index, 0, action_name)
        action_name.textChanged.connect(lambda: action_update_name(action_name, action))

        table.setItem(index, 1, QTableWidgetItem("自定义类型"))

        action_level = QLineEdit()
        action_level.setPlaceholderText("数字，越小越先")
        table.setCellWidget(index, 2, action_level)
        action_level.textChanged.connect(lambda: action_update_level(action_level, action))
        rang = QIntValidator()
        rang.setRange(0, 10)
        action_level.setValidator(rang)

        table.setCellWidget(index, 3, judge_button)
        judge_button.clicked.connect(lambda: self.edit_judge(action))
        action_keys = QLineEdit()
        table.setCellWidget(index, 4, action_keys)
        action_keys.textChanged.connect(lambda: action_update_keys(action_keys, action))
        action_keys.setPlaceholderText("例如：s+d+j")
        table.update()


    def show_actions(self, table,action):
        index = table.rowCount()
        table.insertRow(index)
        judge_button = QPushButton()
        judge_button.setText("编辑")
        action_name = QLineEdit()
        table.setCellWidget(index, 0, action_name)
        action_name.setText(action.name)
        action_name.textChanged.connect(lambda: action_update_name(action_name, action))
        table.setItem(index, 1, QTableWidgetItem("自定义类型"))

        action_level = QLineEdit()
        action_level.setPlaceholderText("数字，越小越先")
        action_level.setText(action.level)
        table.setCellWidget(index, 2, action_level)
        action_level.textChanged.connect(lambda: action_update_level(action_level, action))
        rang = QIntValidator()
        rang.setRange(0, 10)
        action_level.setValidator(rang)

        table.setCellWidget(index, 3, judge_button)
        judge_button.clicked.connect(lambda: self.edit_judge(action))
        action_keys = QLineEdit()
        table.setCellWidget(index, 4, action_keys)
        action_keys.textChanged.connect(lambda: action_update_keys(action_keys, action))
        action_keys.setPlaceholderText("例如：s+d+j")
        action_keys.setText(action.keys)
        table.update()

    # 角度判定设置向量1
    def set_organ1_value(self, angle, value):
        angle.organ1 = str(value.text())

    def set_organ2_value(self, angle, value):
        angle.organ2 = str(value.text())

    def set_organ3_value(self, angle, value):
        angle.organ3 = str(value.text())

    def set_organ4_value(self, angle, value):
        angle.organ4 = str(value.text())

    def set_angle1_value(self, angle, value):
        angle.angle1 = str(value.text())

    def set_angle2_value(self, angle, value):
        angle.angle2 = str(value.text())

    def set_description_value(self, angle, value):
        angle.description = str(value.text())

    def set_judge_point(self, position, value):
        position.judge_point = str(value.text())

    def set_standard_point(self, position, value):
        position.standard = str(value.text())

    def set_located_point(self, position, value):
        position.located = str(value.text())

    def set_position_description_value(self, angle, value):
        angle.description = str(value.text())

    def set_game_name(self, game, value):
        game.name = str(value.text())

    def set_game_description(self, game, value):
        game.description = value.document().toPlainText()

    def set_game_type(self, game, value):
        game.type = value.currentText()

