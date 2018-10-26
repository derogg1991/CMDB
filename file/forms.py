from django import forms

class UpLoadFileForm(forms.Form):
    file = forms.FileField()