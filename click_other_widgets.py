#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/18 21:15
# @Author  : why
# @Email   : mmwhymm@163.com
# @File    : click_other_widgets.py
# @Software: PyCharm
# @Function: xxxx
# @other   :
import time

from PySide6.QtCore import Qt, QRect, QEvent, QPoint, Signal,QSize
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QMouseEvent, QAction, QImage, QPixmap, QIcon
from PySide6.QtWidgets import (QWidget, QApplication, QMenu, QInputDialog,
                               QTableWidgetItem, QStyledItemDelegate, QStyle, QAbstractItemView)

from ui_imagelist import Ui_Dialog as Ui_ImageListDialog
import sys
import os
from pathlib import Path

import mss
import mss.tools
import cv2
import numpy as np


class ImagesListWidget(QWidget,Ui_ImageListDialog):
    get_image_target_Signal = Signal(str,str)
    get_numpy_image_target_Signal = Signal(list,str,str)

    export_final_targets_Signal = Signal(list)

    def __init__(self,main_window_Geo,parent=None):
        super(ImagesListWidget,self).__init__(parent)
        self.setupUi(self)
        self.main_window_geo = main_window_Geo
        self.set_init_position()
        self.set_table_item_size()

        self.images_path_and_action_datas=[]
        self.image_numpy_and_images_path_and_action_datas=[]

        self.get_image_target_Signal.connect(self.get_image_target_func)
        self.get_numpy_image_target_Signal.connect(self.get_numpy_image_target_func)

        self.pushButton_comfirm.clicked.connect(self.transport_final_data)

    def set_table_item_size(self):
        self.tableWidget_targets.setIconSize(QSize(150,150))
        self.tableWidget_targets.setColumnWidth(0,150)
        for i in range(10):
            self.tableWidget_targets.setRowHeight(i,150)

    def set_init_position(self):
        pX = self.main_window_geo.x()
        print(f'Px:{type(pX)}')
        pY = self.main_window_geo.y()
        pW = self.main_window_geo.width()
        pH = self.main_window_geo.height()
        print(f'Py:{pX}')
        self.setGeometry(pX+pW +10,pY,430,600)

    def get_image_target_func(self,image_path:str,action_type:str):
        print(f"imagetable accept:",image_path,':',action_type)
        action ={'image_path':image_path,'action_type':action_type}
        self.images_path_and_action_datas.append(action)

        self.update_images_target_list()

    def get_numpy_image_target_func(self,image_list:list,image_path:str,action_type:str):
        print(f"imagetable accept: {len(image_list)} :",image_path,':',action_type)
        action ={"image_list":image_list,'image_path':image_path,'action_type':action_type}
        self.image_numpy_and_images_path_and_action_datas.append(action)

        self.update_numpy_images_target_list()
        pass


    def update_images_target_list(self):

        for i in self.images_path_and_action_datas:
            print(i)

        data_lenght = len(self.images_path_and_action_datas)

        print(f'图片数据中，已存储{data_lenght} 条记录')

        for row in range(data_lenght):
            # item_image_path = QTableWidgetItem(self.images_path_and_action_datas[row]["image_path"])
            item_image_path = QTableWidgetItem()
            item_image_path.setFlags(Qt.ItemIsEnabled)
            icon = QIcon(self.images_path_and_action_datas[row]["image_path"])

            item_image_path.setIcon(icon)
            image_name = Path(self.images_path_and_action_datas[row]["image_path"]).name
            item_image_name = QTableWidgetItem(image_name)
            item_action_type = QTableWidgetItem(self.images_path_and_action_datas[row]["action_type"])
            row_data = [item_image_path,item_image_name,item_action_type]
            for column in range(3):
                self.tableWidget_targets.setItem(row,column,row_data[column])



    def update_numpy_images_target_list(self):
        "以后会实现的，这种方式希望是将numpy数组转换成图片，而不是需要实际截图。有时间实现吧"
        pass

    def transport_final_data(self):
        self.export_final_targets_Signal.emit(self.images_path_and_action_datas)




class ImageDelegate(QStyledItemDelegate):
    '''据说可以可以将单元格显示图片，但发现直接用QIcon就可以实现，放弃了'''
    def __init__(self, image_path,parent):
        super().__init__()
        self.pixmap = QPixmap(image_path)

    def paint(self, painter, option, index):
        # 在这里绘制图片
        rect = option.rect
        painter.save()
        painter.drawPixmap(rect, self.pixmap.scaled(rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        painter.restore()

    def sizeHint(self):
        # 返回图片的大小作为单元格的大小提示
        return QSize(self.pixmap.size())


class BackgroundWidget(QWidget):
    image_path_and_action_Signal = Signal(str,str)
    image_numpy_and_name_and_action_Signal = Signal(list,str,str) # qt 信号不支持numpy数据，需要转化成list，用的时候需转成numpy数据

    def __init__(self,current_screen:QWidget, parent=None):
        super(BackgroundWidget,self).__init__(parent)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.WindowDoesNotAcceptFocus |
            Qt.Tool)  # 添加这个标志)
        self.screen = current_screen # 获取当前的屏幕
        print(type(self.screen))
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen_geometry = self.screen.geometry()
        # 设置窗口比屏幕小一点（每边缩小1像素）
        self.margin = 1
        new_geometry = QRect(
            screen_geometry.x() + self.margin,
            screen_geometry.y() + self.margin,
            screen_geometry.width() - (self.margin * 2),
            screen_geometry.height() - (self.margin * 2)
        )
        # 设置窗口大小和位置
        self.setGeometry(new_geometry)

        self._start_pos = None
        self._end_pos = None

        self._rect = QRect()

        print(f'全屏开启咯')

        self.make_temp_dir()


    def make_temp_dir(self):
        current_directory = Path.cwd()
        temp_images_dir = current_directory / 'temp'
        if not temp_images_dir.exists():
            temp_images_dir.mkdir()
        else:
            print(f"iamges temp dir: {temp_images_dir}")


    def paintEvent(self,e):
        painter = QPainter(self)
        painter.setOpacity(0.8)  # 设置半透明背景
        painter.fillRect(self.rect(), QColor(00, 0, 0, 200))

        if self._start_pos and self._end_pos:
            # 清除选择区域的遮罩，使其完全透明
            selection_rect = QRect(self._start_pos, self._end_pos).normalized()

            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(selection_rect, Qt.transparent)

            # 绘制选择框的边框
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

            pen = QPen(QColor(255, 0, 0))  # 红色边框
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(QBrush(Qt.NoBrush))

            painter.drawRect(QRect(self._start_pos, self._end_pos).normalized())

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            self._start_pos = event.globalPos() - self.screen.geometry().topLeft() # 需要处理多显示器时加上
            print(f"start pos:{self._start_pos}")
            self._end_pos = self._start_pos
            self.update()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self,event):
        if self._start_pos is not None:
            self._end_pos = event.globalPos() - self.screen.geometry().topLeft()
            print(f"end pos:{self._end_pos}")
            self.update()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self,event):
        if event.button() == Qt.LeftButton:
            self._rect = QRect(self._start_pos, self._end_pos).normalized()
            # 暂时没搞明白，+ self.screen.geometry().topLeft() 这句作用，在全屏画红框的时候是减。
            menu_pos = QPoint(self._rect.x() + self._rect.width() + 10, self._rect.y()) + self.screen.geometry().topLeft()
            self.show_context_menu(menu_pos)
            # self.rect_signal.emit("Ok", self._rect)
            # self.close()
            # self.hide()
            event.accept()
        else:
            super().mouseReleaseEvent(event)


    def grab_chosen_region(self):
        print(f"grab_chosen_region:{self._rect}")

    def show_context_menu(self, pos:QPoint):
        # 创建一个菜单
        menu = QMenu(self)
        # 添加动作到菜单中
        action1 = QAction("点的就是它", self)
        action2 = QAction("双点的就是它(to be continue)", self)
        action3 = QAction("Exit or 按ESC", self)
        action4 = QAction("找的就是它(to be continue)", self).setEnabled(False)
        menu.addAction(action1)
        menu.addAction(action2)
        menu.addSeparator()
        menu.addAction(action3)
        menu.addAction(action4)

        action1.triggered.connect(self.show_input_dialog)
        action1.triggered.connect(self.grab_chosen_region)

        action3.triggered.connect(self.close)
        # 在指定位置显示菜单
        # menu.exec(self.label.mapToGlobal(pos))
        menu.exec(pos)

    def show_input_dialog(self):
        title_text = "命名吧"
        label_text = "给图片命个名"+"\n" + "(尽量用英文,默认png)"
        # 显示输入对话框
        text, ok = QInputDialog.getText(self, title_text, label_text)
        if ok and text:
            time.sleep(0.1)
            # 处理用户输入
            # self.label.setText(f"You entered: {text}")
            print(f"文件名:{text}")

            self.take_chosen_image_into_temp_dir(text)
            self.close()

    def take_chosen_image_into_temp_dir(self,filename):
        File_name = filename + ".png"
        print("保存选择的图片")
        current_directory = Path.cwd()
        temp_images_dir = current_directory / 'temp'
        file_path = temp_images_dir / File_name
        print(f"图片路径为：{file_path}：{type(file_path)}")
        try:
            self.make_chosen_region_into_image(file_path)
            self.image_path_and_action_Signal.emit(file_path.__str__(),"click")
        except Exception as e:
            print("保存图片失败，看看啥原因吧")
            print(e)

        # with file_path.open(mode='w') as f:
        #     f.write("temp text~~~")

    def get_screen_index(self,current_screen):
        '''获取当前屏幕索引，截图需要确认当前的屏幕'''
        app = QApplication.instance()
        screens = app.screens()
        for index, s in enumerate(screens):
            if s.name() == current_screen.name():
                return index
        return -1

    def make_chosen_region_into_image(self,filename):

        chosen_region_rect = self._rect
        region_tuple = (
            chosen_region_rect.y(),
            chosen_region_rect.x(),
            # chosen_region_rect.y(),
            chosen_region_rect.width(),
            chosen_region_rect.height()
        )
        print(f"region_tuple:{region_tuple}")

        current_screen_index = self.get_screen_index(self.screen)

        print(f"current_screen_index:{current_screen_index}")

        with mss.mss() as sct:
            screens = sct.monitors # 获取屏幕列表
            current_screen = screens[current_screen_index+1] # mss的对屏幕的索引需要+1
            print(f"current scrrent: top:{current_screen["top"]},"
                  f"left: {current_screen["left"]},"
                  f"width:{current_screen["width"]},"
                  f"height:{current_screen["height"]}")


            red_line_width = 4 # 为了去掉截图的红色框，需要调整坐标
            monitor_region = {
                # "top": region_tuple[0]+ current_screen["top"],
                # "left": region_tuple[1] + current_screen["left"],
                # "top": (region_tuple[0]+ current_screen["top"])*2,
                # "left": (region_tuple[1] + current_screen["left"])*2,
                "top": (region_tuple[0]+ current_screen["top"])*2 + red_line_width,
                "left": (region_tuple[1] + current_screen["left"])*2 + red_line_width,
                "width": region_tuple[2] *2 - red_line_width,
                "height": region_tuple[3] *2 - red_line_width
            }
            # 以上尺寸非常反直觉。非常神奇，画的红框在全屏下显示正确，但根据框的rect的坐标，需要x,y互换，且需要x2。试了好久才发现。
            # 其实rect 的y 是 top, x是 left。导致第二屏始终不对。我擦嘞，浪费了了2天~~~~

            monitor_region_1 = {
                "top": region_tuple[0]  + current_screen["top"] + red_line_width,
                "left": region_tuple[1] + current_screen["left"] + red_line_width,
                "width": region_tuple[2]  - red_line_width,
                "height": region_tuple[3]  - red_line_width
            }

            if current_screen_index == 0:
                print(f"monitor_region 第一屏幕:{monitor_region}")
                screenshot = sct.grab(monitor_region)
            elif current_screen_index == 1:
                print(f"monitor_region_1 第二屏幕:{monitor_region_1}")
                screenshot = sct.grab(monitor_region_1)

            screen_np = np.array(screenshot)

            # 希望有时间实现利用图片numpy数组，不需要保存图片。
            screen_np_2 = cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)
            screen_np_3 = screen_np_2.tolist()
            self.image_numpy_and_name_and_action_Signal.emit(screen_np_3,filename.__str__(),"click") #

            mss.tools.to_png(screenshot.rgb,screenshot.size,output=filename)





