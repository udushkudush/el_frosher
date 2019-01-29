# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\v.borzenko\Dropbox\inDaHouse\app\UI\submit_form_v2.ui',
# licensing of 'C:\Users\v.borzenko\Dropbox\inDaHouse\app\UI\submit_form_v2.ui' applies.
#
# Created: Thu Jan 24 16:58:50 2019
#      by: pyside2-uic  running on PySide2 5.11.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_submit_dialog(object):
    def setupUi(self, submit_dialog):
        submit_dialog.setObjectName("submit_dialog")
        submit_dialog.resize(352, 202)
        submit_dialog.setSizeGripEnabled(True)
        submit_dialog.setModal(False)
        self.formLayout = QtWidgets.QFormLayout(submit_dialog)
        self.formLayout.setObjectName("formLayout")
        self.autor = QtWidgets.QLabel(submit_dialog)
        self.autor.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.autor.setObjectName("autor")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.autor)
        self.comment = QtWidgets.QTextEdit(submit_dialog)
        self.comment.setMaximumSize(QtCore.QSize(700, 90))
        self.comment.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.comment.setObjectName("comment")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.comment)
        self.stage = QtWidgets.QComboBox(submit_dialog)
        self.stage.setMinimumSize(QtCore.QSize(90, 26))
        self.stage.setObjectName("stage")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.stage)
        self.lineEdit = QtWidgets.QLineEdit(submit_dialog)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 26))
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.confirm_submit = QtWidgets.QPushButton(submit_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.confirm_submit.sizePolicy().hasHeightForWidth())
        self.confirm_submit.setSizePolicy(sizePolicy)
        self.confirm_submit.setMinimumSize(QtCore.QSize(0, 44))
        self.confirm_submit.setMaximumSize(QtCore.QSize(500, 16777215))
        self.confirm_submit.setStyleSheet("")
        self.confirm_submit.setObjectName("confirm_submit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.confirm_submit)

        self.retranslateUi(submit_dialog)
        QtCore.QMetaObject.connectSlotsByName(submit_dialog)

    def retranslateUi(self, submit_dialog):
        submit_dialog.setWindowTitle(QtWidgets.QApplication.translate("submit_dialog", "Dialog", None, -1))
        self.autor.setText(QtWidgets.QApplication.translate("submit_dialog", "autor id", None, -1))
        self.comment.setPlaceholderText(QtWidgets.QApplication.translate("submit_dialog", "type comment here", None, -1))
        self.lineEdit.setPlaceholderText(QtWidgets.QApplication.translate("submit_dialog", "cerebro path to file", None, -1))
        self.confirm_submit.setText(QtWidgets.QApplication.translate("submit_dialog", "SUBMIT", None, -1))

