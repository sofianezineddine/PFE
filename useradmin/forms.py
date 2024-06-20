from core.models import Product
from django import forms
# from bootstrap_datepicker_plus import DatePickerInput



class AddProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Product Title", "class":"form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Product Description", "class":"form-control"}))
    price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "Sale Price", "class":"form-control"}))
    old_price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "Old Price", "class":"form-control"}))
    total_weight = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': "How many Kg are in stock?", "class":"form-control"}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Tags", "class":"form-control"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={"class":"form-control"}))
    color =forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Color", "class":"form-control"}))
    origin =forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Origin", "class":"form-control"}))

    class Meta:
        model = Product
        fields = [
            'title',
            'image',
            'description',
            'price',
            'old_price',
            'specifications',
            'total_weight',
            'tags',
            'category',
            'color',
            'origin'
        ]

        widgets = {
        # 'mdf': DateTimePickerInput
    }