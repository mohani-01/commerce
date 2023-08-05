from django import forms



class NewList(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea())
    price = forms.DecimalField(max_digits=10, decimal_places=2) 
    category = forms.CharField(required=False, max_length=255)
    image = forms.URLField(required=False)
