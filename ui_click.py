# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clickILxXrt.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QRadioButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(430, 300)
        Dialog.setStyleSheet(u"background-color: rgb(233, 255, 233);")
        self.groupBox_statues = QGroupBox(Dialog)
        self.groupBox_statues.setObjectName(u"groupBox_statues")
        self.groupBox_statues.setGeometry(QRect(10, 180, 411, 111))
        self.plainTextEdit_statuszone = QPlainTextEdit(self.groupBox_statues)
        self.plainTextEdit_statuszone.setObjectName(u"plainTextEdit_statuszone")
        self.plainTextEdit_statuszone.setGeometry(QRect(10, 20, 391, 51))
        self.label_start_ = QLabel(self.groupBox_statues)
        self.label_start_.setObjectName(u"label_start_")
        self.label_start_.setGeometry(QRect(10, 80, 91, 21))
        self.label_5 = QLabel(self.groupBox_statues)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(100, 80, 81, 21))
        self.label_6 = QLabel(self.groupBox_statues)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(200, 80, 81, 21))
        self.label_7 = QLabel(self.groupBox_statues)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(290, 80, 81, 21))
        self.groupBox_basesetting = QGroupBox(Dialog)
        self.groupBox_basesetting.setObjectName(u"groupBox_basesetting")
        self.groupBox_basesetting.setGeometry(QRect(10, 90, 411, 80))
        self.pushButton_chosetarget = QPushButton(self.groupBox_basesetting)
        self.pushButton_chosetarget.setObjectName(u"pushButton_chosetarget")
        self.pushButton_chosetarget.setGeometry(QRect(10, 20, 71, 51))
        self.label_frequency = QLabel(self.groupBox_basesetting)
        self.label_frequency.setObjectName(u"label_frequency")
        self.label_frequency.setGeometry(QRect(90, 30, 61, 21))
        self.label_repeattimes = QLabel(self.groupBox_basesetting)
        self.label_repeattimes.setObjectName(u"label_repeattimes")
        self.label_repeattimes.setGeometry(QRect(250, 30, 51, 21))
        self.lineEdit_repeattims = QLineEdit(self.groupBox_basesetting)
        self.lineEdit_repeattims.setObjectName(u"lineEdit_repeattims")
        self.lineEdit_repeattims.setGeometry(QRect(310, 30, 61, 20))
        self.comboBox_frequncy = QComboBox(self.groupBox_basesetting)
        self.comboBox_frequncy.addItem("")
        self.comboBox_frequncy.addItem("")
        self.comboBox_frequncy.addItem("")
        self.comboBox_frequncy.setObjectName(u"comboBox_frequncy")
        self.comboBox_frequncy.setGeometry(QRect(150, 30, 81, 22))
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 411, 71))
        self.horizontalLayoutWidget = QWidget(self.groupBox)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 20, 391, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.radioButton_flowclick = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_flowclick.setObjectName(u"radioButton_flowclick")

        self.horizontalLayout.addWidget(self.radioButton_flowclick)

        self.radioButton_fixedclick = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_fixedclick.setObjectName(u"radioButton_fixedclick")

        self.horizontalLayout.addWidget(self.radioButton_fixedclick)

        self.radioButton_recordrepaly = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_recordrepaly.setObjectName(u"radioButton_recordrepaly")

        self.horizontalLayout.addWidget(self.radioButton_recordrepaly)

        self.radioButton_findimg = QRadioButton(self.horizontalLayoutWidget)
        self.radioButton_findimg.setObjectName(u"radioButton_findimg")
        self.radioButton_findimg.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout.addWidget(self.radioButton_findimg)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox_statues.setTitle(QCoreApplication.translate("Dialog", u"\u72b6\u6001(\u9700\u8981\u9009\u4e2d\u6a21\u5f0f)", None))
        self.plainTextEdit_statuszone.setPlainText(QCoreApplication.translate("Dialog", u"\u5f53\u524d\u6a21\u5f0f \u8ddf\u968f\u70b9\u51fb\n"
"", None))
        self.label_start_.setText(QCoreApplication.translate("Dialog", u"\u5f00\u542f\uff1aShift+K", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u505c\u6b62\uff1aShift+L", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"\u5f55\u5f00\uff1aShift+O", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"\u5f55\u505c\uff1aShift+P", None))
        self.groupBox_basesetting.setTitle(QCoreApplication.translate("Dialog", u"\u57fa\u7840\u8bbe\u7f6e(\u9700\u8981\u9009\u4e2d\u6a21\u5f0f)", None))
        self.pushButton_chosetarget.setText(QCoreApplication.translate("Dialog", u"\u9009\u62e9\u76ee\u6807", None))
        self.label_frequency.setText(QCoreApplication.translate("Dialog", u"\u70b9\u51fb\u9891\u7387", None))
        self.label_repeattimes.setText(QCoreApplication.translate("Dialog", u"\u91cd\u590d\u6b21\u6570", None))
        self.lineEdit_repeattims.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.comboBox_frequncy.setItemText(0, QCoreApplication.translate("Dialog", u"1\u6b21/\u79d2", None))
        self.comboBox_frequncy.setItemText(1, QCoreApplication.translate("Dialog", u"5\u6b21/\u79d2", None))
        self.comboBox_frequncy.setItemText(2, QCoreApplication.translate("Dialog", u"10\u6b21/\u79d2", None))

        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u6a21\u5f0f(\u9009\u4e2d\u540e\u6fc0\u6d3b)", None))
        self.radioButton_flowclick.setText(QCoreApplication.translate("Dialog", u"\u8ddf\u968f\u70b9\u51fb", None))
        self.radioButton_fixedclick.setText(QCoreApplication.translate("Dialog", u"\u56fa\u5b9a\u70b9\u51fb", None))
        self.radioButton_recordrepaly.setText(QCoreApplication.translate("Dialog", u"\u5f55\u5236/\u56de\u653e", None))
        self.radioButton_findimg.setText(QCoreApplication.translate("Dialog", u"\u627e\u56fe\u540e\u70b9\u51fb", None))
    # retranslateUi

