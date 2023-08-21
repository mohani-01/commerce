from django import forms



class NewList(forms.Form):
    title = forms.CharField(label="Title", max_length=64, widget=forms.TextInput(attrs={'placeholder':"Title of your page", "class":"form-control", "id":"newListTitle"}))
    description = forms.CharField(max_length=500, widget=forms.Textarea(attrs={"placeholder": "write a description here.", "class":"form-control", "id":"newListDescription"}), label="Description")
    price = forms.DecimalField(label="Price" ,max_digits=10,  decimal_places=2, widget=forms.NumberInput(attrs={"placeholder":"Put your price here", "class":"form-control"})) 
    image = forms.URLField(label="Image Url", required=False, widget=forms.URLInput(attrs={"placeholder":"URL: https://www.example.com/photos/190819/", "class":"form-control", "autocomplete":"off"}))



class NewBid(forms.Form):
    price = forms.DecimalField(label="", max_digits=10,  decimal_places=2, widget=forms.NumberInput(attrs={"placeholder":"Bid", "class":"bid-input form-control"})) 

class NewComment(forms.Form):
    comment = forms.CharField(label="", widget=forms.TextInput(attrs={ "class":"form-control", "id": "floatingComment", "placeholder":"Add a comment", "autocomplete":"off"}))
