# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\DEV\elFrosh_repo\elFrosher\UI\settings.ui',
# licensing of 'C:\DEV\elFrosh_repo\elFrosher\UI\settings.ui' applies.
#
# Created: Fri Feb  8 18:44:30 2019
#      by: pyside2-uic  running on PySide2 5.11.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_login(object):
    def setupUi(self, login_dialog):
        login_dialog.setObjectName("login_dialog")
        login_dialog.resize(151, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(login_dialog.sizePolicy().hasHeightForWidth())
        login_dialog.setSizePolicy(sizePolicy)
        login_dialog.setMaximumSize(QtCore.QSize(151, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(login_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.user_name = QtWidgets.QComboBox(login_dialog)
        self.user_name.setObjectName("user_name")
        self.verticalLayout.addWidget(self.user_name)
        self.password = QtWidgets.QLineEdit(login_dialog)
        self.password.setObjectName("password")
        self.verticalLayout.addWidget(self.password)
        self.workspace = QtWidgets.QLineEdit(login_dialog)
        self.workspace.setObjectName("workspace")
        self.verticalLayout.addWidget(self.workspace)
        self.confirm = QtWidgets.QPushButton(login_dialog)
        self.confirm.setMinimumSize(QtCore.QSize(0, 36))
        self.confirm.setObjectName("confirm")
        self.verticalLayout.addWidget(self.confirm)

        self.retranslateUi(login_dialog)
        QtCore.QMetaObject.connectSlotsByName(login_dialog)

    def retranslateUi(self, login_dialog):
        login_dialog.setWindowTitle(QtWidgets.QApplication.translate("login_dialog", "Form", None, -1))
        self.password.setPlaceholderText(QtWidgets.QApplication.translate("login_dialog", "password", None, -1))
        self.workspace.setPlaceholderText(QtWidgets.QApplication.translate("login_dialog", "workspace", None, -1))
        self.confirm.setText(QtWidgets.QApplication.translate("login_dialog", "AGA", None, -1))

