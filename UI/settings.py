# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\DEV\elFrosh_repo\elFrosher\UI\settings.ui',
# licensing of 'C:\DEV\elFrosh_repo\elFrosher\UI\settings.ui' applies.
#
# Created: Mon Feb  4 18:21:17 2019
#      by: pyside2-uic  running on PySide2 5.11.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_edit_settings(object):
    def setupUi(self, edit_settings):
        edit_settings.setObjectName("edit_settings")
        edit_settings.resize(151, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(edit_settings.sizePolicy().hasHeightForWidth())
        edit_settings.setSizePolicy(sizePolicy)
        edit_settings.setMaximumSize(QtCore.QSize(151, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(edit_settings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.user_name = QtWidgets.QLineEdit(edit_settings)
        self.user_name.setObjectName("user_name")
        self.verticalLayout.addWidget(self.user_name)
        self.password = QtWidgets.QLineEdit(edit_settings)
        self.password.setObjectName("password")
        self.verticalLayout.addWidget(self.password)
        self.workspace = QtWidgets.QLineEdit(edit_settings)
        self.workspace.setObjectName("workspace")
        self.verticalLayout.addWidget(self.workspace)
        self.confirm = QtWidgets.QPushButton(edit_settings)
        self.confirm.setMinimumSize(QtCore.QSize(0, 36))
        self.confirm.setObjectName("confirm")
        self.verticalLayout.addWidget(self.confirm)

        self.retranslateUi(edit_settings)
        QtCore.QMetaObject.connectSlotsByName(edit_settings)

    def retranslateUi(self, edit_settings):
        edit_settings.setWindowTitle(QtWidgets.QApplication.translate("edit_settings", "Form", None, -1))
        self.user_name.setPlaceholderText(QtWidgets.QApplication.translate("edit_settings", "user name", None, -1))
        self.password.setPlaceholderText(QtWidgets.QApplication.translate("edit_settings", "password", None, -1))
        self.workspace.setPlaceholderText(QtWidgets.QApplication.translate("edit_settings", "workspace", None, -1))
        self.confirm.setText(QtWidgets.QApplication.translate("edit_settings", "AGA", None, -1))

