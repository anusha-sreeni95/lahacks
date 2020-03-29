from django import forms


class UserForm(forms.Form):
    location = forms.CharField(label='Places Visited', max_length=200)
