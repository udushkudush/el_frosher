# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\DEV\elFrosh_repo\elFrosher\UI\create_asset_form.ui',
# licensing of 'C:\DEV\elFrosh_repo\elFrosher\UI\create_asset_form.ui' applies.
#
# Created: Mon Feb  4 18:21:17 2019
#      by: pyside2-uic  running on PySide2 5.11.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 160)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(200, 100))
        Form.setMaximumSize(QtCore.QSize(300, 160))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(-1, 3, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.close_btn = QtWidgets.QPushButton(Form)
        self.close_btn.setText("")
        self.close_btn.setObjectName("close_btn")
        self.horizontalLayout.addWidget(self.close_btn)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.asset_type_cb = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(15)
        sizePolicy.setHeightForWidth(self.asset_type_cb.sizePolicy().hasHeightForWidth())
        self.asset_type_cb.setSizePolicy(sizePolicy)
        self.asset_type_cb.setObjectName("asset_type_cb")
        self.gridLayout.addWidget(self.asset_type_cb, 1, 0, 1, 1)
        self.asset_name_in = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(15)
        sizePolicy.setHeightForWidth(self.asset_name_in.sizePolicy().hasHeightForWidth())
        self.asset_name_in.setSizePolicy(sizePolicy)
        self.asset_name_in.setObjectName("asset_name_in")
        self.gridLayout.addWidget(self.asset_name_in, 1, 1, 1, 1)
        self.create_asset_btn = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.create_asset_btn.sizePolicy().hasHeightForWidth())
        self.create_asset_btn.setSizePolicy(sizePolicy)
        self.create_asset_btn.setObjectName("create_asset_btn")
        self.gridLayout.addWidget(self.create_asset_btn, 2, 0, 1, 2)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 3)
        self.gridLayout.setRowStretch(1, 2)
        self.gridLayout.setRowStretch(2, 4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.asset_name_in.setPlaceholderText(QtWidgets.QApplication.translate("Form", "name asset", None, -1))
        self.create_asset_btn.setText(QtWidgets.QApplication.translate("Form", "CREATE ASSET STRUCTURE", None, -1))

