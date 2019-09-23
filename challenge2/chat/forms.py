from django import forms

class PinForm(forms.Form):
    pin = forms.IntegerField()


class CreateRoomForm(forms.Form):
    name = forms.CharField()
    pin = forms.IntegerField()

class CreateMessageForm(forms.Form):
    message = forms.CharField()
