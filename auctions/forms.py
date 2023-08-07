from django import forms



class NewList(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea())
    price = forms.DecimalField(max_digits=10,  decimal_places=2) 
    image = forms.URLField(required=False)

class NewBid(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2)
class NewComment(forms.Form):
    comment = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":"2", "label":None, "placeholder": "Add Your comment here "}))