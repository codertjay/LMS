from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
# Create your views here.
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic.base import View

from Learning_platform.settings import EMAIL_HOST_USER
from home_page.mixins import InstructorAndLoginRequiredMixin
from .forms import CopyTradeInfoForm
from .models import CopyTradeInfo


# send created mail mail to the user
def copy_trade_created_message(email, name):
    html_message = render_to_string('EmailTemplates/copy_trade_created.html', {'email': email, 'name': name})
    plain_message = strip_tags(html_message)
    send_mail(
        f"AssasinFx Copy Trade ( Created ) ",
        plain_message, EMAIL_HOST_USER, recipient_list=[email, EMAIL_HOST_USER]
        , html_message=html_message, fail_silently=True
    )

    return None


class CopyTradeFormView(View):
    def get(self, request):
        form = CopyTradeInfoForm()
        return render(request, 'HomePage/copy_trade_form/copy_trade_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        print('the post', request.POST)
        form = CopyTradeInfoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            copy_trade_created_message(email=form.cleaned_data.get('email'), name=form.cleaned_data.get('name'))
            messages.success(request, 'You have successfully filled the form, a message has being sent to your mail')
            return redirect('home:home')
        messages.error(request, 'please fill in the form correctly')
        return redirect('home:home')


class CopyTradingdashboardView(InstructorAndLoginRequiredMixin, View):
    def get(self, request):
        copy_trade = CopyTradeInfo.objects.all()
        context = {
            'copy_trade': copy_trade
        }
        return render(request, 'DashBoard/instructor/instructor-copytrading.html', context)

    def post(self, request):
        id = request.POST.get('id')
        if id:
            copy_trade = CopyTradeInfo.objects.filter(id=id).first()
            if copy_trade:
                copy_trade.delete()
                messages.success(request,
                                 'Copy trade has being successfully deleted')
        else:
            messages.warning(request, 'There was an error')
        return redirect('copy_trade:copy_trade_dashboard')
