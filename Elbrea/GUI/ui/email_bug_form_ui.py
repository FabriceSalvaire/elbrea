# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'email_bug_form.ui'
#
# Created: Sun Feb 17 00:13:44 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_email_bug_form(object):
    def setupUi(self, email_bug_form):
        email_bug_form.setObjectName(_fromUtf8("email_bug_form"))
        email_bug_form.setWindowModality(QtCore.Qt.ApplicationModal)
        email_bug_form.resize(1000, 800)
        self.verticalLayout = QtGui.QVBoxLayout(email_bug_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.from_label = QtGui.QLabel(email_bug_form)
        self.from_label.setObjectName(_fromUtf8("from_label"))
        self.verticalLayout.addWidget(self.from_label)
        self.from_line_edit = QtGui.QLineEdit(email_bug_form)
        self.from_line_edit.setObjectName(_fromUtf8("from_line_edit"))
        self.verticalLayout.addWidget(self.from_line_edit)
        self.recipients_label = QtGui.QLabel(email_bug_form)
        self.recipients_label.setObjectName(_fromUtf8("recipients_label"))
        self.verticalLayout.addWidget(self.recipients_label)
        self.recipients_line_edit = QtGui.QLineEdit(email_bug_form)
        self.recipients_line_edit.setWhatsThis(_fromUtf8(""))
        self.recipients_line_edit.setObjectName(_fromUtf8("recipients_line_edit"))
        self.verticalLayout.addWidget(self.recipients_line_edit)
        self.subject_label = QtGui.QLabel(email_bug_form)
        self.subject_label.setObjectName(_fromUtf8("subject_label"))
        self.verticalLayout.addWidget(self.subject_label)
        self.subject_line_edit = QtGui.QLineEdit(email_bug_form)
        self.subject_line_edit.setObjectName(_fromUtf8("subject_line_edit"))
        self.verticalLayout.addWidget(self.subject_line_edit)
        self.description_label = QtGui.QLabel(email_bug_form)
        self.description_label.setObjectName(_fromUtf8("description_label"))
        self.verticalLayout.addWidget(self.description_label)
        self.description_plain_text_edit = QtGui.QPlainTextEdit(email_bug_form)
        self.description_plain_text_edit.setObjectName(_fromUtf8("description_plain_text_edit"))
        self.verticalLayout.addWidget(self.description_plain_text_edit)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cancel_button = QtGui.QPushButton(email_bug_form)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout_2.addWidget(self.cancel_button)
        self.send_email_button = QtGui.QPushButton(email_bug_form)
        self.send_email_button.setObjectName(_fromUtf8("send_email_button"))
        self.horizontalLayout_2.addWidget(self.send_email_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.from_label.setBuddy(self.recipients_line_edit)
        self.recipients_label.setBuddy(self.recipients_line_edit)
        self.subject_label.setBuddy(self.subject_line_edit)
        self.description_label.setBuddy(self.description_plain_text_edit)

        self.retranslateUi(email_bug_form)
        QtCore.QObject.connect(self.cancel_button, QtCore.SIGNAL(_fromUtf8("clicked()")), email_bug_form.reject)
        QtCore.QMetaObject.connectSlotsByName(email_bug_form)
        email_bug_form.setTabOrder(self.subject_line_edit, self.description_plain_text_edit)
        email_bug_form.setTabOrder(self.description_plain_text_edit, self.send_email_button)

    def retranslateUi(self, email_bug_form):
        email_bug_form.setWindowTitle(QtGui.QApplication.translate("email_bug_form", "Email Bug Form", None, QtGui.QApplication.UnicodeUTF8))
        self.from_label.setText(QtGui.QApplication.translate("email_bug_form", "From:", None, QtGui.QApplication.UnicodeUTF8))
        self.from_line_edit.setToolTip(QtGui.QApplication.translate("email_bug_form", "Type your email, for example \"john.doe@company.com\"", None, QtGui.QApplication.UnicodeUTF8))
        self.recipients_label.setText(QtGui.QApplication.translate("email_bug_form", "Additional Recipients:", None, QtGui.QApplication.UnicodeUTF8))
        self.recipients_line_edit.setToolTip(QtGui.QApplication.translate("email_bug_form", "Type something like \"john.doe@company.com,jean.dupont@company.com,...\"", None, QtGui.QApplication.UnicodeUTF8))
        self.subject_label.setText(QtGui.QApplication.translate("email_bug_form", "Subject:", None, QtGui.QApplication.UnicodeUTF8))
        self.subject_line_edit.setToolTip(QtGui.QApplication.translate("email_bug_form", "Type a short description", None, QtGui.QApplication.UnicodeUTF8))
        self.description_label.setText(QtGui.QApplication.translate("email_bug_form", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_button.setText(QtGui.QApplication.translate("email_bug_form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.send_email_button.setText(QtGui.QApplication.translate("email_bug_form", "Send", None, QtGui.QApplication.UnicodeUTF8))

