from django import forms


class NewListing(forms.Form):
    name = forms.CharField(label="Title", max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Name of Item'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write your description about the object'}))
    # bid = forms.IntegerField(label="Starting bid", widget=forms.NumberInput(attrs={'placeholder': 'Your starting bid'}))