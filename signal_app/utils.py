from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.utils.html import strip_tags

from django.template.loader import render_to_string

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


# send created mail mail to the user
def signal_created_message(signal):
    html_message = render_to_string('main/signal_created_message.html', {'signal': signal})
    plain_message = strip_tags(html_message)
    # send message to the user
    send_mail(
        f"AssasinFx Signal ( Created ) ",
        plain_message, EMAIL_HOST_USER
        [signal.user.email], html_message=html_message
    )
    # send message to admin
    send_mail(
        f"{signal.user.first_name} - {signal.user.last_name} Signal Was Created ",
        plain_message, signal.user.email
        [EMAIL_HOST_USER], html_message=html_message
    )

    return None


# send mail to the user
def signal_expired_message(signal):
    html_message = render_to_string('main/signal_expired_message.html', {'signal': signal})
    plain_message = strip_tags(html_message)
    # send signal message to the user that his signal has being expired
    send_mail(
        f"AssasinFx Signal ( Expired ) ",
        plain_message, EMAIL_HOST_USER
        [signal.user.email], html_message=html_message
    )
    # send signal message  to admin that user signal has being expired
    send_mail(
        f"{signal.user.first_name} - {signal.user.last_name} Signal Expired ",
        plain_message, signal.user.email
        [EMAIL_HOST_USER], html_message=html_message
    )
    return None
