from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


# send created mail mail to the user
def copy_trading_created_message(copy_trade):
    print('this is the copy_trade', copy_trade.user)
    html_message = render_to_string('main/copy_trade_created_message.html', {'copy_trade': copy_trade})
    plain_message = strip_tags(html_message)
    print('the copy_trade email', copy_trade.user.email)
    copy_trade_email = copy_trade.user.email
    # send message to the user and admin
    send_mail(
        f"AssasinFx Copy trade ( Created ) ",
        plain_message, EMAIL_HOST_USER, recipient_list=[copy_trade_email, EMAIL_HOST_USER]
        , html_message=html_message, fail_silently=True
    )

    return None


# send mail to the user
def copy_trading_expired_message(copy_trade):
    html_message = render_to_string('main/copy_trade_expired_message.html', {'copy_trade': copy_trade})
    plain_message = strip_tags(html_message)
    # send copy_trade message to the user that his copy_trade has being expired
    copy_trade_email = copy_trade.user.email

    send_mail(
        f"AssasinFx Copy trade ( Expired ) ",
        plain_message, EMAIL_HOST_USER
        , recipient_list=[copy_trade_email, EMAIL_HOST_USER], html_message=html_message, fail_silently=True
    )
    return None
