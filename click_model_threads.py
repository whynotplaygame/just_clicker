#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/12 07:25
# @Author  : why
# @Email   : mmwhymm@163.com
# @File    : click_model_threads.py
# @Software: PyCharm
# @Function: xxxx
# @other   :
# from PySide6.QtGui import Key
from signal import signal

from pynput import keyboard
from pynput.mouse import Controller as mc
from pynput.mouse import Button
from pynput.mouse import Listener as mouse_listener
import time
import mss
import numpy as np
import cv2
from pathlib import Path
import datetime

# from threading import Thread

from PySide6.QtCore import Qt, QRect, Signal, QObject, Slot,QThread
from PySide6.QtWidgets import QMessageBox

# 各个模式通用的键盘命令监听
class KeyBoardListener(QThread):
    comand_signal = Signal(str)
    def __init__(self,parent=None):
        super(KeyBoardListener, self).__init__()
        self.running = True
        # self.current_keys = set()

        # 定义一个字典来存储当前按下的修饰键
        self.current_modifiers = {
            'ctrl': False,
            'alt': False,
            'shift': False
        }

        self.keyboard_listener = None


    def run(self):
        print("KeyBoardListener is new running~")

        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)

        print(f"{self.keyboard_listener}: listenerddd ")
        self.keyboard_listener.start()
        self.keyboard_listener.join()


    def stop(self):
        self.running = False
        print("KeyBoardListener is stopped~ in 监听线程")
        self.keyboard_listener.stop()


    def on_press(self, key):
        print(f"someone key pressed~")
        try:
            # self.current_keys.add(key)
            # print(f'{[i for i in current_keys]} pressed')
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.current_modifiers['ctrl'] = True
                print("ctrl pressed")
            elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                self.current_modifiers['alt'] = True
                print("alt pressed")
            elif key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
                self.current_modifiers['shift'] = True
                print("shift pressed")
            else:
                # 检查是否按下了组合键（例如 Ctrl+C）
                if self.current_modifiers['shift'] and key.char == 'K':
                    print("shift+k pressed")
                    self.comand_signal.emit("start")

                elif self.current_modifiers['shift'] and key.char == 'L':
                    print("shift+l pressed")
                    self.comand_signal.emit("close")
                # 可以添加更多组合键的判断
                elif self.current_modifiers['shift'] and key.char == 'O':
                    print("shift+O pressed")
                    self.comand_signal.emit("record")
                # 可以添加更多组合键的判断
                elif self.current_modifiers['shift'] and key.char == 'P':
                    print("shift+P pressed")
                    self.comand_signal.emit("stop_record")
                # 可以添加更多组合键的判断
                else:
                    print("emit nothing")
                    self.comand_signal.emit("nothing~~")
        except AttributeError:
            pass

    def on_release(self, key):
        print(f"{key} is released")

        try:
            if key == keyboard.Key.ctrl:
                print("ctrl release")
                self.current_modifiers['ctrl'] = False
            elif key == keyboard.Key.alt:
                print("alt release")
                self.current_modifiers['alt'] = False
            elif key == keyboard.Key.shift:
                print("shift release")
                self.current_modifiers['shift'] = False
            elif key == keyboard.Key.esc:
                print("esc release")
                self.comand_signal.emit("cancel")
        except AttributeError:
            pass

#-------------------------为了跟随点击模式
class FlowClickThread(QThread):
    def __init__(self, interval:float,parent=None):
        super().__init__(parent)
        self.running = True
        self.interval = interval
        self.mouse_controller = None
        print("flowclickthread is created~")

    # def start(self): # 莫名其妙，必须重写下start()方法
    #     self.run()

    def run(self):
        print("flowclickthread is running~")
        # for i in range(10):
        while self.running:
            print("i am clicking!")

            mouse_controller = mc()
            mouse_controller.press(Button.left)
            mouse_controller.release(Button.left)

            time.sleep(self.interval)

    def stop(self):
        self.running = False
        if self.mouse_controller:
            self.mouse_controller = None

#-------------------------为了固定点击模式
class FixedClickChoseTargetThread(QThread):
    '''
    用于固定点击目标搜索的线程类
    '''
    mouse_signal = Signal(str,tuple)
    def __init__(self):
        super().__init__()
        self.running = True
        self.listener = None

    def run(self):
        counter = 0
        print(f"update thread self.running: {self.running}")
        if self.running:
            print("----2----")
            self.track_mouse()

    # pynput 监听鼠标移动
    def on_move(self,x, y):
        print(f"Mouse moved to ({x}, {y})")
        self.mouse_signal.emit(f"Mousemoved_to",(round(x), round(y)))

    # pynput 监听鼠标点击
    def on_click(self,x,y,button,pressed):
        print(f"Mouse clicked at ({x}, {y}) with {button}")
        self.mouse_signal.emit(f"Mouseclicked_at",(round(x), round(y)))

    # 监听鼠标移动和点击
    def track_mouse(self):
        if not self.running:
            return
        """监听鼠标移动"""
        # with mouse.Listener(on_move=self.on_move) as listener:
        #     listener.join()
        self.listener = mouse_listener(on_move=self.on_move,on_click=self.on_click)
        self.listener.start()
        self.listener.join()

        time.sleep(1)

    def stop(self):
        if self.listener:
            self.listener.stop()
        print(f"update thread self.running: {self.running}")

class FixedClickThread(QThread):
    def __init__(self,interval:float,repeat_times:int,position:tuple,parent=None):
        super().__init__()
        self.running = True
        self.interval = interval
        self.repeat_times = repeat_times
        self.position = position

    def run(self):
        mouse_controller = mc()
        print(f"position: {self.position[0]} is {type(self.position[0])}")
        for i in range(self.repeat_times):
            if self.running:
                mouse_controller.position = (self.position[0], self.position[1])
                print(f"move to {self.position}")
                print("i am clicking fixed!")
                mouse_controller.press(Button.left)
                mouse_controller.release(Button.left)
                time.sleep(self.interval)
            else:
                print("提前结束，跳出循环")
                break
        print("顺利完成点击")

    def stop(self):
        self.running = False

#-------------------------为了录制播放模式
class Action:
    '''
    鼠标动作类
    '''
    def __init__(self,action_type:str,action_data:str):
        self.action_type = action_type
        self.action_data = action_data

class RecorderThread(QThread):
    recorder_result = Signal(list)

    def __init__(self,parent=None):
        super().__init__()
        self.mouse_record_list = []
        self.listener = None
        self.running = True
        self.sampling_rate = 1 # 采样频率

    def run(self):
        print(f"update thread self.running: {self.running}")
        if self.running:
            self.track_mouse()

    # pynput 监听鼠标移动
    def on_move(self,x, y):
        print(f"Mouse moved to ({x}, {y})")
        # self.signal.emit(f"Mousemoved_to ({round(x)}, {round(y)})")
        action = Action("move",(round(x),round(y)))
        self.mouse_record_list.append(action)

    # pynput 监听鼠标点击
    def on_click(self,x,y,button,pressed):
        print(f"Mouse clicked at ({x}, {y}) with {button}")
        # self.signal.emit(f"Mouseclicked_at ({round(x)}, {round(y)}) with {button}")
        action = Action("click",(round(x),round(y)))
        self.mouse_record_list.append(action)

    # 监听鼠标移动和点击
    def track_mouse(self):
        if not self.running:
            return
        """监听鼠标移动"""
        self.listener = mouse_listener(on_move=self.on_move,on_click=self.on_click)
        self.listener.start()
        self.listener.join()
        #time.sleep(self.sampling_rate)


    def stop(self):
        self.running = False
        if self.listener:
            self.listener.stop()
        self.recorder_result.emit(self.mouse_record_list) # 停止的时候，发送记录信号


class ReplayerThread(QThread):
    def __init__(self,record_data:list,repeat_times:int,parent=None):
        super().__init__()
        self.record_data = record_data
        self.repeat_times = repeat_times

        self.running = True

    def run(self):
        mouse_controller = mc()
        if self.running:
            print(f"重放参数：数据：{self.record_data},次数：{self.repeat_times}")
            for i in range(self.repeat_times):
                if not self.running: # 由于有次数限制，需要在执行操作步骤前，判断是否继续。
                    break
                for step in self.record_data:
                    if step.action_type == "move":
                        print(f"control mouse move to {step.action_data}")
                        mouse_controller.position = (step.action_data[0], step.action_data[1])
                        time.sleep(0.01)
                    elif step.action_type == "click":
                        print(f"control mouse click at {step.action_data}")
                        mouse_controller.press(Button.left)
                        mouse_controller.release(Button.left)
                        time.sleep(0.01)

    def stop(self):
        self.running = False


#-------------------------为了找图模式
class CreateImageTargetTaskThread(QThread):
    operate_status = Signal(int)
    operates_task_list = Signal(list)

    def __init__(self,parent=None):
        self.running = True

    def run(self):
        if self.running:
            pass

    def stop(self):
        self.running = False
        pass



class FindAndOperateImageTargetThread(QThread):
    '''
    由于模板匹配的时候，要求在当前屏幕下，且模板都是刚截的图，就不考虑匹配时，对于多尺寸的匹配支持
    暂时只是支持单个目标匹配
    对于目前的这个匹配算法，在同样大小下，优先匹配与模版颜色一致的。
    暂时不做特征匹配，感觉不太适合精准定位。
    已经确定可以成功接直接利用传过来的numpy数据来定位，不用本地实际图片形式。正常可以方便用简单方案形式了。不用依托图片。
    还是先用实际图片实现吧。
    '''

    exe_status_signal = Signal(str)

    execute_strategy ={
        "think_time": 1, # 每一步间隔时间
        "attempt_times":3, # 重试次数
        "continue_next":True # 失败次数够时候，是否继续，True 继续，False 直接结束
    }
    def __init__(self,targets_data:list,repeat_times:int,current_screen_index:int,parent=None):
        super().__init__()
        self.running = True
        self.targets_data = targets_data
        self.repeat_times = repeat_times
        self.current_screen_index = current_screen_index

        self.interval = 1

    def run(self):
        if self.running:
            for i in range(self.repeat_times):
                print(f"第{i}轮找图")
                if not self.running:
                    break
                print(f"我找图点击线程要开始干活了！","\n",f"活儿：{self.targets_data}","\n",f"次数:{self.repeat_times}")
                for j in range(len(self.targets_data)):
                    time.sleep(self.execute_strategy["think_time"]) # 进入每一个图，还是要稍微等一下。
                    if not self.running:
                        break
                    result,top_left,bottom_right,fail_continue = self.execute_find_img_step_with_strategy(j)
                    if not result and fail_continue: # 如果没找到，且 失败继续为true,则继续找下一个图了。
                        print("没找到这个图，继续找一下吧")
                        continue
                    elif not result and not fail_continue:
                        print("找不到算了。剩下的也不找了")
                        break

                    print(result,top_left,bottom_right,fail_continue)
                    self.execute_operation(top_left,bottom_right)


    def execute_operation(self,top_left:tuple,bottom_right:tuple, click_times = 1):

        offset_x_for_second_screen = 0
        offset_y_for_second_screen = 0
        with mss.mss() as sct:
            screen_index_real = self.current_screen_index + 1
            print(f"current monitor: {screen_index_real}")
            monitor = sct.monitors[screen_index_real]
            offset_y_for_second_screen = monitor["top"]
            offset_x_for_second_screen = monitor["left"]

        print(f"current offset y: {offset_x_for_second_screen} and x: {offset_y_for_second_screen}")
        # 讲真，这块x，y,top,left 不是很清晰。都是尝试出来的。有时间得整理下。目前是好使的。
        mouse_controller = mc()
        position_x = top_left[0] + int((bottom_right[0] - top_left[0]) / 2) + offset_x_for_second_screen
        position_y = top_left[1] + int((bottom_right[1] - top_left[1])  / 2) + offset_y_for_second_screen
        mouse_controller.position = (position_x, position_y)
        print(f"move to px:{position_x} : py: {position_y}")
        print("i am clicking image!!!")
        click_times = 1
        for i in range(click_times):
            print("i am clicking image!!!")
            mouse_controller.press(Button.left)
            mouse_controller.release(Button.left)
            # time.sleep(self.interval)


    def execute_find_img_step_with_strategy(self,image_index: int):
        print(f"找第{image_index}个图咯")
        att_tims = self.execute_strategy["attempt_times"]
        result = False
        top_left = None
        bottom_right = None
        fail_continue = False
        while att_tims:
            print(f"还剩几次呢：{att_tims}")
            result, top_left, bottom_right = self.trans_image_target_into_position_and_action(image_index)
            if result:
                print("我找到了。")
                break
            else:
                time.sleep(self.execute_strategy["think_time"])
                print("上一次没找到，休息1s后继续")
                att_tims = att_tims - 1
                print(f"还剩下{att_tims}次")

                if att_tims == 0 and self.execute_strategy["continue_next"]:
                    fail_continue = True
                    print(f"尝试次数{self.execute_strategy['attempt_times']}后仍未找到，继续找下一个图")

                continue

        return result, top_left, bottom_right, fail_continue



    def trans_image_target_into_position_and_action(self,image_index:int):
        screen = self.capture_screen(self.current_screen_index)
        target_template = self.load_template_target(self.targets_data[image_index]["image_path"])
        top_left, bottom_right, confidence = self.match_template(screen,target_template)
        print(f"左上：{top_left},右下：{bottom_right},可信度：{confidence}")
        print(f"可信度：{type(confidence)} >>> {confidence}")
        if confidence > 0.8: # 实测超过80%,基本就是靠谱了。以后在走配置吧
            print("找到了")
            return True,top_left,bottom_right
        else:
            print("没找到啊")
            return False,None,None


    def capture_screen(self,screen_index:int):
        with mss.mss() as sct:
            screen_index_real = screen_index + 1
            print(f"current monitor: {screen_index_real}")
            monitor = sct.monitors[screen_index_real]
            screenshot = sct.grab(monitor)
            screen_np = np.array(screenshot)
            screen_np_2 = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
            return screen_np_2

    def load_template_target(self, image_target_path:str):
        correct_path = Path(image_target_path)
        print(correct_path)
        # correct_path = r".\temp\feifeifei.png"
        # 加载模板图像
        try:
            #template = cv2.imread(image_path_for_chinese_issue, cv2.IMREAD_COLOR)
            # template_2 = cv2.cvtColor(template, cv2.COLOR_BGR2RGB)
            # 由于中文路径不可避免，需要用字节流的方式去加载图片
            image_path_for_chinese_issue = cv2.imdecode(np.fromfile(correct_path,dtype=np.uint8),cv2.IMREAD_COLOR)
            if image_path_for_chinese_issue is None:
                print(f"无法读取图片 {correct_path}")
            # 左上：(730, 566), 右下：(940, 610), 可信度：0.9419190287590027
            # 我草咧。COLOR_RGB2BGR  这个很关键。cv2.COLOR_BGR2GRAY：会导致颜色判断错误。改成COLOR_RGB2BGR 会解决这个问题
            # 图片预处理，降噪，增强都不好使。就是因为这个破玩意儿。草。耽误了一天。
            # 迫不得已，打个方向还试对了。
            image_path_for_chinese_issue_2 = cv2.cvtColor(image_path_for_chinese_issue,cv2.COLOR_RGB2BGR)
            return image_path_for_chinese_issue_2
        except Exception as e:
            print(e)
            return None

    def match_template(self,screen, template):

        # 进行模板匹配
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 获取匹配位置
        top_left = max_loc
        h, w, _ = template.shape
        bottom_right = (top_left[0] + w, top_left[1] + h)

        return top_left, bottom_right, max_val


    def stop(self):
        self.running = False
        pass



if __name__ == '__main__':
    # test()
    time.sleep(3)
    print("开始点击")
    # t1 = time.time()
    # clicking(mouse_controller,True,1)
    # FlowClickThreadObject = FlowClickThread(0.5)
    # FlowClickThreadObject.start()
    # test()
    # print(f"线程开启在{t1}")
    # t2 = time.time()
    # print(f"完成10次所需时间{t2-t1}")
    # time.sleep(20)
    # print("20s后结束线程")
    # FlowClickThreadObject.stop()
    # FlowClickThreadObject.join()
    # a = KeyBoardListener()
    # a.run()

    # b = FixedClickChoseTargetThread()
    # b.run()
    c = RecorderThread()
    c.run()

