# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_issue_form.ui'
#
# Created: Sun Feb 17 00:13:43 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_new_issue_form(object):
    def setupUi(self, new_issue_form):
        new_issue_form.setObjectName(_fromUtf8("new_issue_form"))
        new_issue_form.setWindowModality(QtCore.Qt.ApplicationModal)
        new_issue_form.resize(1000, 800)
        self.verticalLayout = QtGui.QVBoxLayout(new_issue_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.subject_label = QtGui.QLabel(new_issue_form)
        self.subject_label.setObjectName(_fromUtf8("subject_label"))
        self.verticalLayout.addWidget(self.subject_label)
        self.subject_line_edit = QtGui.QLineEdit(new_issue_form)
        self.subject_line_edit.setObjectName(_fromUtf8("subject_line_edit"))
        self.verticalLayout.addWidget(self.subject_line_edit)
        self.description_label = QtGui.QLabel(new_issue_form)
        self.description_label.setObjectName(_fromUtf8("description_label"))
        self.verticalLayout.addWidget(self.description_label)
        self.description_plain_text_edit = QtGui.QPlainTextEdit(new_issue_form)
        self.description_plain_text_edit.setObjectName(_fromUtf8("description_plain_text_edit"))
        self.verticalLayout.addWidget(self.description_plain_text_edit)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cancel_button = QtGui.QPushButton(new_issue_form)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout_2.addWidget(self.cancel_button)
        self.ok_button = QtGui.QPushButton(new_issue_form)
        self.ok_button.setObjectName(_fromUtf8("ok_button"))
        self.horizontalLayout_2.addWidget(self.ok_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.subject_label.setBuddy(self.subject_line_edit)
        self.description_label.setBuddy(self.description_plain_text_edit)

        self.retranslateUi(new_issue_form)
        QtCore.QObject.connect(self.cancel_button, QtCore.SIGNAL(_fromUtf8("clicked()")), new_issue_form.reject)
        QtCore.QMetaObject.connectSlotsByName(new_issue_form)
        new_issue_form.setTabOrder(self.subject_line_edit, self.description_plain_text_edit)
        new_issue_form.setTabOrder(self.description_plain_text_edit, self.ok_button)

    def retranslateUi(self, new_issue_form):
        new_issue_form.setWindowTitle(QtGui.QApplication.translate("new_issue_form", "New Issue Form", None, QtGui.QApplication.UnicodeUTF8))
        self.subject_label.setText(QtGui.QApplication.translate("new_issue_form", "Subject:", None, QtGui.QApplication.UnicodeUTF8))
        self.subject_line_edit.setToolTip(QtGui.QApplication.translate("new_issue_form", "Type a short description", None, QtGui.QApplication.UnicodeUTF8))
        self.description_label.setText(QtGui.QApplication.translate("new_issue_form", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_button.setText(QtGui.QApplication.translate("new_issue_form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_button.setText(QtGui.QApplication.translate("new_issue_form", "Ok", None, QtGui.QApplication.UnicodeUTF8))

