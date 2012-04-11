from django.core.mail.message import EmailMultiAlternatives

from school_food_site import settings

def mail_followers(school, subject, message):
    followers = school.followers.all()
    if not followers:
        return
    email_addresses = [follower.user.email for follower in followers]
    _mail_multiple(subject, message, email_addresses)

def _mail_multiple_personalized(subject, messages, fail_silently=False, connection=None, html_message=None):
    for email, message in messages.items():
        _mail_multiple(subject, message, [email], fail_silently=fail_silently, connection=connection, html_message=html_message)

def _mail_multiple(subject, message, email_addresses, fail_silently=False, connection=None, html_message=None):
    """Sends a message to multiple email addresses. Based on django.core.mail.mail_admins()"""
    for email_address in email_addresses:
        mail = EmailMultiAlternatives(u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject), message, from_email=settings.SERVER_EMAIL,
                                      to=[email_address], connection=connection, bcc=settings.MANAGERS)
        if html_message:
            mail.attach_alternative(html_message, 'text/html')
        mail.send(fail_silently=fail_silently)
