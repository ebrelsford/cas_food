from django.template.loader import render_to_string

from notify.mail import mail_multiple

class Notifier(object):
    def __init__(self, subject_template=None, text_template=None):
        self.subject_template = subject_template
        self.text_template = text_template

    def get_context(self):
        """
        Get the context to include when rendering the notification templates
        """
        return {}

    def get_receivers(self):
        """
        Get the receivers (of type User) who should receive this notification
        """
        raise NotImplementedError

    def _get_receiver_addresses(self):
        return [user.email for user in self.get_receivers()]

    def send(self, extra_context={}):
        """Send the notifications"""
        context = self.get_context()
        context.update(extra_context)
        mail_multiple(render_to_string(self.subject_template, context).strip(),
                      render_to_string(self.text_template, context),
                      self._get_receiver_addresses())

class FollowerNotifier(Notifier):
    def get_followers(self):
        raise NotImplementedError

    def get_receivers(self):
        return self.get_followers()

class NewTrayNotifier(FollowerNotifier):
    def __init__(self, tray, subject_template='notify/new_tray_subject.txt',
                 text_template='notify/new_tray_text.txt'):
        super(NewTrayNotifier, self).__init__(
            subject_template=subject_template,
            text_template=text_template)
        self.tray = tray

    def get_context(self):
        context = super(NewTrayNotifier, self).get_context()
        context.update(dict(tray=self.tray))
        return context

    def get_followers(self):
        return [profile.user for profile in self.tray.school.followers.all()]

class NewNoteNotifier(FollowerNotifier):
    def __init__(self, note, subject_template='notify/new_note_subject.txt',
                 text_template='notify/new_note_text.txt'):
        super(NewNoteNotifier, self).__init__(
            subject_template=subject_template,
            text_template=text_template)
        self.note = note

    def get_context(self):
        context = super(NewNoteNotifier, self).get_context()
        context.update(dict(note=self.note))
        return context

    def get_followers(self):
        return [profile.user for profile in self.note.content_object.followers.all()]
