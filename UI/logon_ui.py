# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\DEV\projects\xueta\elFrosher\UI\logon_UI.ui',
# licensing of 'C:\DEV\projects\xueta\elFrosher\UI\logon_UI.ui' applies.
#
# Created: Mon Feb 11 00:02:41 2019
#      by: pyside2-uic  running on PySide2 5.11.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(325, 153)
        self.verticalLayout = QtWidgets.QVBoxLayout(Login)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.server = QtWidgets.QLineEdit(Login)
        self.server.setObjectName("server")
        self.horizontalLayout_2.addWidget(self.server)
        self.srv_connect = QtWidgets.QPushButton(Login)
        self.srv_connect.setObjectName("srv_connect")
        self.horizontalLayout_2.addWidget(self.srv_connect)
        self.horizontalLayout_2.setStretch(0, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.user = QtWidgets.QComboBox(Login)
        self.user.setObjectName("user")
        self.horizontalLayout.addWidget(self.user)
        self.password = QtWidgets.QLineEdit(Login)
        self.password.setObjectName("password")
        self.horizontalLayout.addWidget(self.password)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.workspace = QtWidgets.QLineEdit(Login)
        self.workspace.setObjectName("workspace")
        self.verticalLayout.addWidget(self.workspace)
        self.accept = QtWidgets.QPushButton(Login)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.accept.sizePolicy().hasHeightForWidth())
        self.accept.setSizePolicy(sizePolicy)
        self.accept.setMinimumSize(QtCore.QSize(0, 32))
        self.accept.setMaximumSize(QtCore.QSize(16777215, 48))
        self.accept.setObjectName("accept")
        self.verticalLayout.addWidget(self.accept)
        self.verticalLayout.setStretch(3, 2)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        Login.setWindowTitle(QtWidgets.QApplication.translate("Login", "Dialog", None, -1))
        self.server.setPlaceholderText(QtWidgets.QApplication.translate("Login", "enter server path", None, -1))
        self.srv_connect.setText(QtWidgets.QApplication.translate("Login", "cnct", None, -1))
        self.workspace.setPlaceholderText(QtWidgets.QApplication.translate("Login", "workspace", None, -1))
        self.password.setPlaceholderText(QtWidgets.QApplication.translate("Login", "enter password", None, -1))
        self.accept.setText(QtWidgets.QApplication.translate("Login", "AGA", None, -1))

