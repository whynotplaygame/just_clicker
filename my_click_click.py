'''
Author: why vvwhyvv@163.com
Date: 2024-10-14 18:21:38
LastEditors: why vvwhyvv@163.com
LastEditTime: 2024-10-14 18:26:41
FilePath: /suibian/pyside6Test/my_click_click.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys
from signal import signal
from wsgiref.validate import validator

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QObject, QThread, Signal, QTimer, QEventLoop, QEvent, QPoint,QRect
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtGui import QIntValidator

# from pyside6Test.click_other_widgets import BackgroundWidgetTest
from ui_click import Ui_Dialog
from click_other_widgets import ImagesListWidget,BackgroundWidget

from enum import Enum
from click_model_threads import (KeyBoardListener,FlowClickThread,
                                 FixedClickChoseTargetThread,FixedClickThread,
                                 RecorderThread,ReplayerThread,
                                 FindAndOperateImageTargetThread)


# 组件的枚举
class Components(Enum):
    RADIO_FLOW = 0 # 跟随点击
    RADIO_FIXED = 1 # 固定点击
    RADIO_RECORD = 2 # 录制回放
    RADIO_FIND_IMG = 3  # 找图
    BUTTON_CHOSE_TARGET = 4 # 选择目标按钮
    COMBO_FREQUNCY_TEXT = 5 # 点击频率文字
    COMBO_FREQUNCY_ = 6 # 点击频率
    EDIT_REPEAT_TEXT = 7 # 重复次数框文字
    EDIT_REPEAT = 8 # 重复次数框
    EDIT_STATUS = 9 # 状态框

modoel_disable_dic ={"Default":[Components.BUTTON_CHOSE_TARGET.value,
                   Components.EDIT_REPEAT_TEXT.value,
                   Components.EDIT_REPEAT.value,
                   Components.COMBO_FREQUNCY_TEXT.value,
                   Components.COMBO_FREQUNCY_.value,
                   Components.EDIT_STATUS.value],
                      "Flow":[Components.BUTTON_CHOSE_TARGET.value,Components.
                      EDIT_REPEAT_TEXT.value,Components.EDIT_REPEAT.value],
                      "Fixed":[],
                      "RECORD":[Components.BUTTON_CHOSE_TARGET.value,
                                Components.COMBO_FREQUNCY_TEXT.value,
                                Components.COMBO_FREQUNCY_.value],
                      "FIND_IMG":[Components.COMBO_FREQUNCY_TEXT.value,
                                  Components.COMBO_FREQUNCY_.value]}

# 不同模式下，需要disable的组件不同
class ClickModel(QObject):
    model_name:str = ""

class DefaultClickModel(QObject):
    disable_list =[Components.BUTTON_CHOSE_TARGET.value,
                   Components.EDIT_REPEAT_TEXT.value,
                   Components.EDIT_REPEAT.value,
                   Components.COMBO_FREQUNCY_TEXT.value,
                   Components.COMBO_FREQUNCY_.value,
                   Components.EDIT_STATUS.value]

class FlowClickModel(ClickModel):

    def __init__(self):#,frequncey_num:float):
        super().__init__()
        print("跟随点击创建")
        self.frequncey_nums= 0
        self.repeat_times = 0 # 占位用，方便切换频率时，一起触发修改实例属性，否则报错
        self.KeyBoardListenerThread = KeyBoardListener()
        self.KeyBoardListenerThread.comand_signal.connect(self.work_command)
        self.hasStarted = False


    def work_command(self,com:Signal):
        print(f"new signal is: {com}")
        if com == "start":
            print(f"传入的频率：{self.frequncey_nums}")
            self.FlowClickThread = FlowClickThread(self.frequncey_nums) # 接收到信号后再创建点击线程
            self.hasStarted = True
            self.FlowClickThread.start()
        elif com == "close":
            print("try to close clicking")
            if self.hasStarted:
                self.FlowClickThread.stop()
                self.FlowClickThread.wait()


    def active(self):
        print("跟随模式激活")
        self.KeyBoardListenerThread.start()


    def close(self):
        print("跟随模式关闭ing")
        if self.hasStarted:
            print("点击线程存在，关闭点击线程")
            self.FlowClickThread.stop()
            self.FlowClickThread.wait()
        print("开始关闭监听线程")
        self.KeyBoardListenerThread.stop()
        self.KeyBoardListenerThread.wait()
        print("跟随模式关闭")


class FixedClickModel(ClickModel):
    status_signal = Signal(str,tuple) # 用于传递

    def __init__(self):
        super().__init__()
        print("固定点击创建")
        self.chose_target_thread = FixedClickChoseTargetThread() # 实例化搜索线程
        self.chose_target_thread.mouse_signal.connect(self.get_chosen_target) # 搜索线程连接槽函数
        self.hasStartedChoseTarget = False # 标记搜索目标线程是否开启的状态
        self.chosen_target_position:tuple = None

        self.frequncey_nums = 0
        self.repeat_times = 0
        self.hasStarted = False

        self.KeyBoardListenerThread = KeyBoardListener()
        self.KeyBoardListenerThread.comand_signal.connect(self.work_command)


    def work_command(self,com:str):
        print(f"new signal is: {com}")
        if com == "start":
            print(f"频率：{self.frequncey_nums},次数{self.repeat_times}，位置{self.chosen_target_position}")
            self.FixedClickThread = FixedClickThread(self.frequncey_nums,self.repeat_times,self.chosen_target_position) # 接收到信号后再创建点击线程
            self.hasStarted = True
            self.FixedClickThread.start()
        elif com == "close":
            print("try to close clicking")
            if self.hasStarted:
                self.FixedClickThread.stop()
                self.FixedClickThread.wait()

    def boot_chose_target_thread(self):
        '''
        用于启动搜索线程
        :return:
        '''
        if not self.hasStartedChoseTarget:
            print("未开启搜索线程，则开启")
            self.chose_target_thread.start()
            self.hasStartedChoseTarget = True
        else:
            pass
            # 用于测试
            # print("已开启搜索线程，则关闭")
            # self.chose_target_thread.stop()
            # self.chose_target_thread.wait()
            # self.hasStartedChoseTarget = False

    def get_chosen_target(self,mouse_action_type:str,mouse_action_position:tuple):
        '''
        1，用于搜索线程的位置信号
        2，用于发射搜索线程状态给主界面
        3，用于获取搜索线程点击信号的坐标，用于执行点击
        :param mouse_action_type:
        :param mouse_action_position:
        :return:
        '''
        print(mouse_action_type,mouse_action_position)
        self.status_signal.emit(mouse_action_type,mouse_action_position)
        if mouse_action_type == "Mouseclicked_at": # 当点下时，停止搜索线程
            self.chosen_target_position = mouse_action_position
            print(f"已选择的点击目标坐标为：{self.chosen_target_position}")
            print("已开启搜索线程，则关闭")
            self.chose_target_thread.stop()
            self.chose_target_thread.wait()
            self.hasStartedChoseTarget = False
        pass

    def active(self):
        print("固定模式激活")
        self.KeyBoardListenerThread.start()
        pass

    def close(self):
        print("关闭固定点击模式")
        if self.hasStarted:
            self.FixedClickThread.stop()
            self.FixedClickThread.wait()
        print("开始关闭监听线程")
        self.KeyBoardListenerThread.stop()
        self.KeyBoardListenerThread.wait()
        print("跟随模式关闭")

class RecordClickModel(ClickModel):
    status_signal = Signal(str) # 录制，播放等传给主界面的信号
    mouse_record = Signal(str) # 鼠标做动作记录传给主界面的信号

    def __init__(self):
        super().__init__()
        print("录制点击创建")

        self.KeyBoardListenerThread = KeyBoardListener()
        self.KeyBoardListenerThread.comand_signal.connect(self.work_command)

        self.frequncey_nums = 0 # 对这个模式没意义，只是为了占位，保证修改这个属性时不会报错

        self.hasStarted = False # 是否正在执行
        self.recording = False # 是否正在录制
        self.repeat_times = 0 # 重复次数

        self.recoder_data =[]  # 需要播放的记录


    def work_command(self,com:str):
        print(f"new signal is: {com}")
        if com == "start":
            print(f"次数{self.repeat_times}")
            self.ReplayerThread = ReplayerThread(self.recoder_data,self.repeat_times) # 接收到信号后再创建点击线程
            self.hasStarted = True
            self.ReplayerThread.start()
            self.status_signal.emit("replaying~")
        elif com == "close":
            print("try to close clicking")
            self.status_signal.emit("closing~")
            if self.hasStarted:
                self.ReplayerThread.stop()
                self.ReplayerThread.wait()
        elif com == "record":
            self.RecorderThread = RecorderThread()
            self.RecorderThread.recorder_result.connect(self.get_recorder_result)
            self.recording = True
            self.RecorderThread.start()
            self.status_signal.emit("recording")
            print("启动录制线程")
        elif com == "stop_record":
            print("停止录制线程")
            # self.status_signal.emit("record stopped~")
            # self.mouse_record_for_show_status()
            if self.recording:
                print("尝试停止录制中的线程")
                self.RecorderThread.stop()
                self.mouse_record_for_show_status()
                self.RecorderThread.wait()
            pass

    def get_recorder_result(self,record_result:list):
        self.recoder_data = record_result # 接收来自录制线程的结果信号，赋值

    def mouse_record_for_show_status(self):
        step_details_str = ''
        for i in range(len(self.recoder_data)):
            temp = f"{i}:{self.recoder_data[i].action_type},position:{self.recoder_data[i].action_data}"
            print(temp)
            step_details_str = step_details_str + temp +'\n'
        print(step_details_str)
        self.mouse_record.emit(step_details_str) # 把鼠标记录数据传出去

    def active(self):
        print("录制模式激活")
        self.KeyBoardListenerThread.start() # 启动键盘监听线程
        pass

    def close(self):
        print("录制模式关闭")
        if self.hasStarted:
            print("尝试关闭重放线程")
            self.ReplayerThread.stop()
            self.ReplayerThread.wait()
        self.KeyBoardListenerThread.stop()
        self.KeyBoardListenerThread.wait()


class FindIMGClickModel(ClickModel):
    status_signal = Signal(str)  # 录制，播放等传给主界面的信号

    def __init__(self,current_screen:QWidget,current_app_geo):
        super().__init__()
        print("找图点击创建")
        self.KeyBoardListenerThread = KeyBoardListener()
        self.KeyBoardListenerThread.comand_signal.connect(self.work_command)

        self.current_screen = current_screen
        self.BackgroudWidget = BackgroundWidget(self.current_screen)

        self.current_app_geo = current_app_geo

        self.targets_list = [] # 用于保存从图片目标列表窗口的最终数据列表，用于初始化 重放任务 线程
        self.repeat_times = 0
        self.hasStarted = False

        self.BackgroudWidget.image_path_and_action_Signal.connect(self.show_images)
        self.BackgroudWidget.image_numpy_and_name_and_action_Signal.connect(self.show_np_images)

        self.ImagesListWidget = ImagesListWidget(self.current_app_geo) # 创建图片列表框
        self.ImagesListWidget.export_final_targets_Signal.connect(self.get_final_targets_data_from_image_list)


    def work_command(self,com:str):
        print(f"new signal is: {com}")
        if com == "start":
            print(f"次数{self.repeat_times}")
            self.FindAndOperateImageTargetThread = FindAndOperateImageTargetThread(
                self.targets_list,
                self.repeat_times,
                self.get_screen_index(self.current_screen)) # 接收到信号后再创建点击线程
            self.hasStarted = True
            self.FindAndOperateImageTargetThread.start()
            self.status_signal.emit("replaying~")
        elif com == "close":
            print("try to close clicking")
            self.status_signal.emit("closing~")
            if self.hasStarted:
                self.FindAndOperateImageTargetThread.stop()
                self.FindAndOperateImageTargetThread.wait()
        elif com == "cancel":
            self.BackgroudWidget.close()

    def boot_search_image_targets_worker(self):
        print("开启查找目标喽")
        self.BackgroudWidget.show()

    def show_images(self,img_path,action_type):
        print(img_path)
        print(action_type)
        self.ImagesListWidget.get_image_target_Signal.emit(img_path,action_type)

    def get_final_targets_data_from_image_list(self,data:list):
        self.targets_list = data
        print(f"来自于图片目标列表的数据： {self.targets_list}")

    def show_np_images(self,np_list,img_path,action_type):
        print(len(np_list),':',img_path,':',action_type)
        # print(np_list,':',img_path,':',action_type)
        self.ImagesListWidget.get_numpy_image_target_Signal.emit(np_list,img_path,action_type)

    def get_screen_index(self,current_screen):
        '''获取当前屏幕索引，截图需要确认当前的屏幕'''
        app = QApplication.instance()
        screens = app.screens()
        for index, s in enumerate(screens):
            if s.name() == current_screen.name():
                return index
        return -1

    def active(self):
        print("找图模式激活")
        self.ImagesListWidget.show()
        self.KeyBoardListenerThread.start()
        pass

    def close(self):
        print("录制模式关闭")
        if self.BackgroudWidget:
            self.BackgroudWidget.close()
        if self.ImagesListWidget:
            self.ImagesListWidget.close()
        self.KeyBoardListenerThread.stop()
        self.KeyBoardListenerThread.wait()



class MyWidget(QWidget,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("mymouse")
        # 隐藏标题栏,常驻
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.pushButton_chosetarget.clicked.connect(self.printT)
        self.components = [self.radioButton_flowclick,
                           self.radioButton_fixedclick,
                           self.radioButton_recordrepaly,
                           self.radioButton_findimg,
                           self.pushButton_chosetarget,
                           self.label_frequency,
                           self.comboBox_frequncy,
                           self.label_repeattimes,
                           self.lineEdit_repeattims,
                           self.plainTextEdit_statuszone] # 所有组件的列表，与枚举排序一致

        validator_for_repeattimes = QIntValidator(0,999,self)
        self.lineEdit_repeattims.setValidator(validator_for_repeattimes)


        self.radioButton_flowclick.toggled.connect(self.radiobutton_flowclick)
        self.radioButton_fixedclick.toggled.connect(self.radiobutton_fixedclick)
        self.radioButton_recordrepaly.toggled.connect(self.radiobutton_recordclick)
        self.radioButton_findimg.toggled.connect(self.radiobutton_findimg)

        self.current_mode = None
        self.current_active_mode = None # 激活模式后，赋值给它，便于将获取当前设置内容，传给相应的模式的属性

        self.current_frequncy = 0
        self.repeat_times = 0
        self.comboBox_frequncy.currentIndexChanged.connect(self.change_current_frequncy) # 频率设置变化时，连接槽函数
        self.lineEdit_repeattims.textChanged.connect(self.change_current_repeate) # 重复次数文本发生变化时，连接槽函数
        self.default_model()


    def default_model(self):
        '''
        默认启动第一个模式，且将组件状态设为第一模式的disable状态
        :return:
        '''
        print(f"组件个数：{len(self.components)}")
        # self.radioButton_flowclick.setChecked(True)
        self.disable_components_for_model(-1)
        # self.active_model(Components.RADIO_FLOW.value)
        self.current_mode = Components.RADIO_FLOW.value
        self.current_frequncy = 1.0
        self.lineEdit_repeattims.setText("10")
        print(f"current mode: {self.current_mode}")

    def change_current_frequncy(self,index):
        if index == 0:
            self.current_frequncy = 1.0
            print(f"set current frequncy {self.current_frequncy}")

        elif index == 1:
            self.current_frequncy = 0.5
            print(f"set current frequncy {self.current_frequncy}")

        elif index == 2:
            self.current_frequncy = 0.1
            print(f"set current frequncy {self.current_frequncy}")

        self.current_active_mode.frequncey_nums = self.current_frequncy

    def get_current_frequncy(self):
        return self.current_frequncy

    def change_current_repeate(self,index):
        print("重复次数发生变化")
        if self.current_active_mode:
            self.current_active_mode.repeat_times = int(self.lineEdit_repeattims.text())

    def disable_components_for_model(self,active_radio:int):
        '''
        将不同模式下的组件隐藏
        :param active_radio:
        :return:
        '''
        for i in range(len(self.components)):
            temp_model_disable_list = None # 只用于显示，跟逻辑无关切换后直接删除
            if active_radio == -1:
                temp_model_disable_list = modoel_disable_dic["Default"]
            elif active_radio == Components.RADIO_FLOW.value:
                temp_model_disable_list = modoel_disable_dic["Flow"]
                # temp_model = FlowClickModel(0)
            elif active_radio == Components.RADIO_FIXED.value:
                temp_model_disable_list = modoel_disable_dic["Fixed"]
                # temp_model = FixedClickModel()
            elif active_radio == Components.RADIO_RECORD.value:
                temp_model_disable_list = modoel_disable_dic["RECORD"]
                # temp_model = RecordClickModel()
            elif active_radio == Components.RADIO_FIND_IMG.value:
                temp_model_disable_list = modoel_disable_dic["FIND_IMG"]
                #temp_model = FindIMGClickModel()

            # print(f"{temp_model_disable_list}:list")

            if i in temp_model_disable_list:
                self.components[i].setEnabled(False)
                self.components[i].setHidden(True)
                # print(f"{i} list other")
            else:
                self.components[i].setEnabled(True)
                self.components[i].setHidden(False)

            del temp_model_disable_list


    def radiobutton_flowclick(self,checked):
        # self.FlowClickModel = None
        if checked == True:
            print("flow mode 按钮被切换开启")
            self.disable_components_for_model(Components.RADIO_FLOW.value)
            self.current_mode = Components.RADIO_FLOW.value
            print(f"current mode: {self.current_mode}")
            print(f"current frequency: {self.current_frequncy} 进行初始化跟随Mode")
            # self.FlowClickModel = FlowClickModel(self.current_frequncy)
            self.FlowClickModel = FlowClickModel()
            self.current_active_mode = self.FlowClickModel
            # self.FlowClickModel.active()
            self.current_active_mode.active()
            self.current_active_mode.frequncey_nums = self.current_frequncy # 切入模式后，先获取当前的频率设置
            self.plainTextEdit_statuszone.setPlainText("跟随点击模式，随走随点")

        elif checked == False:
            print("flow mode 按钮被切换关闭")
            if self.current_active_mode:
                print("尝试关闭模式")
                self.current_active_mode.close()
                self.current_active_mode = None
            print("flow mode over~")


    def radiobutton_fixedclick(self,checked):
        if checked == True:
            print("fix mode~")
            self.disable_components_for_model(Components.RADIO_FIXED.value)
            self.current_mode = Components.RADIO_FIXED.value
            print(f"current mode: {self.current_mode}")
            self.fixedmode = FixedClickModel()
            self.current_active_mode = self.fixedmode
            self.pushButton_chosetarget.clicked.connect(self.current_active_mode.boot_chose_target_thread)
            self.current_active_mode.status_signal.connect(self.show_fixedmode_status)
            self.current_active_mode.active()
            self.current_active_mode.frequncey_nums = self.current_frequncy # 切入模式后，先获取当前的频率设置
            self.current_active_mode.repeat_times = int(self.lineEdit_repeattims.text())
            self.plainTextEdit_statuszone.setPlainText("固定点击模式，固定位置点点点")
        elif checked == False:
            print("fixed mode 按钮被切换关闭")
            self.pushButton_chosetarget.clicked.disconnect(self.current_active_mode.boot_chose_target_thread)
            if self.current_active_mode:
                print("尝试关闭模式")
                self.current_active_mode.close()
                self.current_active_mode = None
            print("fixed mode over~")

    def radiobutton_recordclick(self,checked):
        if checked == True:
            print("record mode~")
            self.disable_components_for_model(Components.RADIO_RECORD.value)
            self.current_mode = Components.RADIO_RECORD.value
            print(f"current mode: {self.current_mode}")
            self.recordmode = RecordClickModel()
            self.current_active_mode = self.recordmode
            self.current_active_mode.active()
            self.current_active_mode.status_signal.connect(self.show_recordmode_status)
            self.current_active_mode.mouse_record.connect(self.show_mouserecord_status)
            self.current_active_mode.repeat_times = int(self.lineEdit_repeattims.text())
            self.plainTextEdit_statuszone.setPlainText("录制回放模式，录制后回放")

        elif checked == False:
            print("record/replay mode 按钮被切换关闭")
            if self.current_active_mode:
                print("尝试关闭模式")
                self.current_active_mode.close()
                self.current_active_mode = None
            print("record/replay mode over~")

    def radiobutton_findimg(self,checked):
        self.imagelistWidget = None
        if checked == True:
            print("find img mode~")
            self.disable_components_for_model(Components.RADIO_FIND_IMG.value)
            self.current_mode = Components.RADIO_FIND_IMG.value
            print(f"current mode: {self.current_mode}")

            # self.imagelistWidget = ImagesListWidget(self.geometry())
            # self.imagelistWidget.show()

            self.FindIMGClickModel = FindIMGClickModel(self.screen(),self.geometry())
            self.current_active_mode = self.FindIMGClickModel
            self.current_active_mode.active()
            self.pushButton_chosetarget.clicked.connect(self.current_active_mode.boot_search_image_targets_worker)
            # self.current_active_mode.current_screen = self.screen() # 把 当前屏幕传给模式类，方便处理多屏幕
            #self.current_active_mode.BackgroudWidget = BackgroundWidget(self.screen())
            self.current_active_mode.status_signal.connect(self.show_recordmode_status)
            self.current_active_mode.repeat_times = int(self.lineEdit_repeattims.text())
            self.plainTextEdit_statuszone.setPlainText("找图点击，找图后后点击")

        elif checked == False:
            print("找图点击模式被切换关闭")
            self.pushButton_chosetarget.clicked.disconnect(self.current_active_mode.boot_search_image_targets_worker)
            if self.current_active_mode.BackgroudWidget:
                self.current_active_mode.BackgroudWidget.close()
            if self.current_active_mode:
                print("尝试关闭模式")
                self.current_active_mode.close()
                self.current_active_mode = None
            print("找图点击模式被切换关闭 over~")


    def printT(self):
        print("hhee")
        # self.current_active_mode.boot_chose_target_thread()

    def show_fixedmode_status(self,mat:str,map:tuple):
        '''
        为了固定位置点击状态显示
        :param mat:
        :param map:
        :return:
        '''
        txt =f"{mat} in x: {map[0]},y: {map[1]}"
        self.plainTextEdit_statuszone.setPlainText(txt)
        pass

    def show_recordmode_status(self,recordmode_status:str):
        self.plainTextEdit_statuszone.setPlainText(recordmode_status)

    def show_mouserecord_status(self,mouse_record:str):
        txt = f"传过来的鼠标行为记录:" + '\n' + mouse_record
        self.plainTextEdit_statuszone.setPlainText(txt)

    def keyboardComandFunc(self,commad:str):
        print(f"{commad}:command")







if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet('''
    QPushButton:pressed {
        background-color:white;
    }
    QPushButton:hover {
        background-color: "red";
        font-size: 15px;
    }
    QPushButton:focus {
        background-color: "blue";
    }
    ''')
    MyWidget = MyWidget()
    MyWidget.show()
    sys.exit(app.exec())