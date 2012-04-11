from django.core.mail.message import EmailMultiAlternatives

from school_food_site import settings

def mail_multiple(subject, message, email_addresses, fail_silently=False, connection=None, html_message=None):
    """Sends a message to multiple email addresses. Based on django.core.mail.mail_admins()"""
    for email_address in email_addresses:
        mail = EmailMultiAlternatives(u'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject), message, from_email=settings.SERVER_EMAIL,
                                      to=[email_address], connection=connection, bcc=settings.MANAGERS)
        if html_message:
            mail.attach_alternative(html_message, 'text/html')
        mail.send(fail_silently=fail_silently)
