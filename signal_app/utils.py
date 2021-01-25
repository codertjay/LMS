from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.utils.html import strip_tags

from django.template.loader import render_to_string

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


def signal_expired_message(signal):
    html_message = render_to_string('main/signal_expired_message.html', {'signal': signal})
    plain_message = strip_tags(html_message)
    send_mail(
        "Signal Expired ",
        plain_message, EMAIL_HOST_USER
        [signal.user.email], html_message=html_message
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

