import logging

from django.http import HttpResponse
from django.views import View
from.models import AppLePay


def apple_pay_merchant_domain_association(request):
    status = 200
    content = AppLePay.objects.first().content
    if not content:
        content = 'Apple Pay is not configured for Assassinfx.'
        # 501 Not Implemented -- https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.2
        return HttpResponse(status=501, content=content, content_type="text/plain")
    return HttpResponse(content, content_type="text/plain", status=200)
