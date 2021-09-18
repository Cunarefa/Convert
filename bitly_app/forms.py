from django import forms


class LongURLForm(forms.Form):
    long_url = forms.CharField(max_length=500, widget=forms.TextInput(
                    attrs={"class": 'form-control', "placeholder": "Shorten your link"}))