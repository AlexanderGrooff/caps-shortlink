from django import forms


class ShortenerForm(forms.Form):
    long_url = forms.CharField(max_length=10000, label='LONG UNCAPSED URL', required=True)
