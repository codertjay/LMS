from django import forms

from copy_trading.models import CopyTradeInfo, Yes_or_No, account_type


class CopyTradeInfoForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    account_type = forms.ChoiceField(widget=forms.TextInput(attrs={'class': 'form-control'}), choices=account_type)
    account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    broker = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    Broker_server = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice_of_symbols = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    slippage = forms.ChoiceField(label='Slippage', widget=forms.RadioSelect(attrs={'class': 'form-control '}),
                                 choices=Yes_or_No)
    forex_pairs = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': '  '}),
                                    choices=Yes_or_No)
    indices = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': ''}), choices=Yes_or_No)
    metals = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': ''}), choices=Yes_or_No)

    class Meta:
        model = CopyTradeInfo
        fields = '__all__'
