from django.template.loader import render_to_string

from accounts.mail import mail_followers

class NewTrayNotifier(object):
    subject_template = 'notify/new_tray_subject.txt'
    text_template = 'notify/new_tray_text.txt'

    def __init__(self, tray, subject_template=None, text_template=None):
        self.tray = tray
        if subject_template:
            self.subject_template = subject_template
        if text_template:
            self.text_template = text_template

    def send(self, extra_context={}):
        context = dict(tray=self.tray)
        context.update(extra_context)
        mail_followers(self.tray.school, 
                       render_to_string(self.subject_template, context).strip(),
                       render_to_string(self.text_template, context) )
