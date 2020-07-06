# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.plainTextEdit_Message = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_Message.setObjectName(u"plainTextEdit_Message")
        self.plainTextEdit_Message.setGeometry(QRect(10, 520, 671, 41))
        self.pushButton_SendMessage = QPushButton(self.centralwidget)
        self.pushButton_SendMessage.setObjectName(u"pushButton_SendMessage")
        self.pushButton_SendMessage.setGeometry(QRect(700, 500, 91, 31))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_SendMessage.sizePolicy().hasHeightForWidth())
        self.pushButton_SendMessage.setSizePolicy(sizePolicy)
        self.pushButton_BrowsFile = QPushButton(self.centralwidget)
        self.pushButton_BrowsFile.setObjectName(u"pushButton_BrowsFile")
        self.pushButton_BrowsFile.setGeometry(QRect(700, 530, 91, 31))
        sizePolicy.setHeightForWidth(self.pushButton_BrowsFile.sizePolicy().hasHeightForWidth())
        self.pushButton_BrowsFile.setSizePolicy(sizePolicy)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(380, 10, 121, 20))
        self.pushButton_Connect = QPushButton(self.centralwidget)
        self.pushButton_Connect.setObjectName(u"pushButton_Connect")
        self.pushButton_Connect.setGeometry(QRect(510, 10, 75, 23))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 47, 13))
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(60, 10, 51, 20))
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(10, 60, 781, 421))
        self.plainTextEdit.setReadOnly(True)
        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(170, 10, 113, 20))
        self.lineEdit_3.setReadOnly(True)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(130, 10, 31, 20))
        self.pushButton_StartListen = QPushButton(self.centralwidget)
        self.pushButton_StartListen.setObjectName(u"pushButton_StartListen")
        self.pushButton_StartListen.setGeometry(QRect(60, 30, 75, 23))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(600, 10, 190, 19))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.radioButton_ECB = QRadioButton(self.layoutWidget)
        self.radioButton_ECB.setObjectName(u"radioButton_ECB")
        self.radioButton_ECB.setChecked(True)

        self.horizontalLayout.addWidget(self.radioButton_ECB)

        self.radioButton_CBC = QRadioButton(self.layoutWidget)
        self.radioButton_CBC.setObjectName(u"radioButton_CBC")

        self.horizontalLayout.addWidget(self.radioButton_CBC)

        self.radioButton_CFB = QRadioButton(self.layoutWidget)
        self.radioButton_CFB.setObjectName(u"radioButton_CFB")

        self.horizontalLayout.addWidget(self.radioButton_CFB)

        self.radioButton_OFB = QRadioButton(self.layoutWidget)
        self.radioButton_OFB.setObjectName(u"radioButton_OFB")

        self.horizontalLayout.addWidget(self.radioButton_OFB)

        self.layoutWidget1 = QWidget(self.centralwidget)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 570, 774, 23))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.progressBar = QProgressBar(self.layoutWidget1)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(700, 0))
        self.progressBar.setValue(24)

        self.horizontalLayout_2.addWidget(self.progressBar)

        self.label_sendFile = QLabel(self.centralwidget)
        self.label_sendFile.setObjectName(u"label_sendFile")
        self.label_sendFile.setGeometry(QRect(10, 500, 671, 20))
        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.plainTextEdit_Message, self.pushButton_SendMessage)
        QWidget.setTabOrder(self.pushButton_SendMessage, self.pushButton_BrowsFile)
        QWidget.setTabOrder(self.pushButton_BrowsFile, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.lineEdit)
        QWidget.setTabOrder(self.lineEdit, self.pushButton_Connect)
        QWidget.setTabOrder(self.pushButton_Connect, self.radioButton_CFB)
        QWidget.setTabOrder(self.radioButton_CFB, self.radioButton_OFB)
        QWidget.setTabOrder(self.radioButton_OFB, self.radioButton_ECB)
        QWidget.setTabOrder(self.radioButton_ECB, self.radioButton_CBC)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_SendMessage.setText(QCoreApplication.translate("MainWindow", u"Send message", None))
        self.pushButton_BrowsFile.setText(QCoreApplication.translate("MainWindow", u"Browse file", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"127.0.0.1:5001", None))
        self.pushButton_Connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"my port", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"5004", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"my IP", None))
        self.pushButton_StartListen.setText(QCoreApplication.translate("MainWindow", u"start listen", None))
        self.radioButton_ECB.setText(QCoreApplication.translate("MainWindow", u"ECB", None))
        self.radioButton_CBC.setText(QCoreApplication.translate("MainWindow", u"CBC", None))
        self.radioButton_CFB.setText(QCoreApplication.translate("MainWindow", u"CFB", None))
        self.radioButton_OFB.setText(QCoreApplication.translate("MainWindow", u"OFB", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"sending file...", None))
        self.label_sendFile.setText(QCoreApplication.translate("MainWindow", u"Send file:", None))
    # retranslateUi

