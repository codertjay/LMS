from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


def signal_expired_message(signal):
    template = get_template('main/signal_expired_message.html')
    content = template.render(signal)
    send_mail(
        "Signal Expired ",
        content,
        signal.user.email,
        [EMAIL_HOST_USER],
        fail_silently=True,
    )
    return None


def signal_created_message(signal):
    template = get_template('main/signal_created_message.html')
    content = template.render(signal)
    send_mail(
        "Signal Created ",
        content,
        signal.user.email,
        [EMAIL_HOST_USER],
        fail_silently=True,
    )
    return None
