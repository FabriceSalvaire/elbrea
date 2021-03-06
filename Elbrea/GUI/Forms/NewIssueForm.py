####################################################################################################
# 
# XXXXX - XXXXX
# Copyright (C) 2015 - XXXXX
# 
####################################################################################################

####################################################################################################

from PyQt5 import QtCore, QtWidgets

####################################################################################################

from Elbrea.Tools.Platform import Platform
from Elbrea.Tools.RedmineRest import RedmineRest
import Elbrea.Config.Config as Config

####################################################################################################

from .ui.new_issue_form_ui import Ui_new_issue_form

####################################################################################################

class NewIssueForm(QtWidgets.QDialog):

    ###############################################

    def __init__(self, traceback=''):

        super(NewIssueForm, self).__init__()

        self._traceback = traceback

        form = self.form = Ui_new_issue_form()
        form.setupUi(self)

        form.ok_button.clicked.connect(self.commit_new_issue)

    ##############################################

    def commit_new_issue(self):

        form = self.form

        subject = str(form.subject_line_edit.text())

        template_description = '''
Bug description:
%(description)s

---------------------------------------------------------------------------------
%(platform)s
---------------------------------------------------------------------------------

%(traceback)s
---------------------------------------------------------------------------------
'''   

        platform = Platform() # Fixme: singleton ?

        description = template_description % {'description': str(form.description_plain_text_edit.toPlainText()),
                                              'platform': str(platform),
                                              'traceback': self._traceback,
                                              }

        redmine_rest = RedmineRest(url=Config.RedmineRest.url,
                                   key=Config.RedmineRest.key)

        elbrea_project = redmine_rest.get_project(Config.RedmineRest.project)

        elbrea_project.new_issue(subject=subject,
                                description=description,
                                priority_id=None,
                                tracker_id=None,
                                assigned_to_id=None,
                                user_data=None)

        self.accept()

####################################################################################################
#
# End
#
####################################################################################################
