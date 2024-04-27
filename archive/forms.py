from django import forms
from .models import Country, ArchivedItem  # İhtiyacınız olan modelleri belirtin

class Form1(forms.Form):
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)
    image4 = forms.ImageField(required=False)
    image5 = forms.ImageField(required=False)
    image6 = forms.ImageField(required=False)
    image7 = forms.ImageField(required=False)
    image8 = forms.ImageField(required=False)
    image9 = forms.ImageField(required=False)
    name = forms.EmailField(max_length=50)
    url = forms.URLField(max_length=200)
    country = forms.ModelMultipleChoiceField(queryset=Country.objects.all(), required=False)
    txID = forms.CharField(max_length=200)  # txID'nin maksimum uzunluğunu gereksinime uygun olarak ayarlayın
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        # Burada ad için özel bir kontrol yapabilirsiniz, örneğin boş olup olmadığını kontrol edin
        if not name:
            raise forms.ValidationError("Name cannot be empty.")
        return name

    def clean_url(self):
        url = self.cleaned_data.get('url')
        # URL validasyonu burada yapılabilir, örneğin URL formatını kontrol edin
        if not url.startswith('http://') and not url.startswith('https://'):
            raise forms.ValidationError("Enter a valid URL.")
        return url



class Form2(forms.Form):
    name = forms.EmailField(max_length=50)
    block = forms.IntegerField()
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter item delete password'}),
        help_text="Your item's password"
    )

    def query_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("E-mail cannot be empty.")

    def query_pw(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Password cannot be empty.")
        