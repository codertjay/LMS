from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View


class SignalRegisterView(View):
    def post(self):
        return redirect('home:home')


class SignalView(View):
