# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'imagelistgqfvws.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(430, 600)
        Dialog.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        Dialog.setStyleSheet(u"background-color: rgb(233, 255, 233);")
        self.tableWidget_targets = QTableWidget(Dialog)
        if (self.tableWidget_targets.columnCount() < 3):
            self.tableWidget_targets.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_targets.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_targets.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_targets.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.tableWidget_targets.rowCount() < 11):
            self.tableWidget_targets.setRowCount(11)
        self.tableWidget_targets.setObjectName(u"tableWidget_targets")
        self.tableWidget_targets.setGeometry(QRect(0, 40, 401, 561))
        self.label_limited_text = QLabel(Dialog)
        self.label_limited_text.setObjectName(u"label_limited_text")
        self.label_limited_text.setGeometry(QRect(90, 10, 321, 20))
        self.pushButton_comfirm = QPushButton(Dialog)
        self.pushButton_comfirm.setObjectName(u"pushButton_comfirm")
        self.pushButton_comfirm.setGeometry(QRect(10, 2, 81, 31))
        self.pushButton_comfirm.setStyleSheet(u"border-color: rgb(221, 29, 255);\n"
"color: rgb(255, 113, 30);\n"
"background-color: rgb(178, 255, 62);")

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"ImageTargets", None))
        ___qtablewidgetitem = self.tableWidget_targets.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"\u56fe\u7247\u76ee\u6807", None));
        ___qtablewidgetitem1 = self.tableWidget_targets.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"\u56fe\u7247\u540d", None));
        ___qtablewidgetitem2 = self.tableWidget_targets.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"\u884c\u4e3a", None));
        self.label_limited_text.setText(QCoreApplication.translate("Dialog", u"\u6ce8\u610f\uff01\u5f53\u524d\u6700\u9ad8\u652f\u630110\u6761\u54df\uff01\u4e00\u822c\u6765\u8bf4\u7b80\u5355\u9700\u6c42\u591f\u4f60\u7528\u4e86\u5427\uff01", None))
        self.pushButton_comfirm.setText(QCoreApplication.translate("Dialog", u"\u5c31\u8fd9\u4e9b\u4e86\uff01", None))
    # retranslateUi

