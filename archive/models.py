from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import random
import string

class BusinessLine(models.Model):
    name = models.CharField(max_length=50) 
    image = models.ImageField(upload_to='static/images/bussiness')

class Country(models.Model):
    name = models.CharField(max_length=50) 

class tx_ID(models.Model):
    name = models.CharField(max_length=100) 

class ArchivedItem(models.Model):
    name = models.EmailField(max_length=50)
    password = models.CharField(max_length=128)
    image = models.ImageField(upload_to='static/images/items')
    url = models.URLField()
    price = models.IntegerField(default=10)
    country = models.ManyToManyField(Country)   
    txID = models.CharField(max_length=200)
    pointGroup = models.ForeignKey('pointGroup', related_name='items', on_delete=models.CASCADE, null=True)

    def reset_item(self):
        self.password = make_password(self.generate_random_password())
        
        # Eğer resim dosyası varsa sil, ImageField'ı boşalt
        if self.image:
            self.image.delete(save=False)  # Resmi sil
            self.image = None  # ImageField'ı boşalt
        self.name = ""
        self.url = ""
        self.price = 10  # Fiyatı varsayılan değere sıfırla
        self.country.clear()  # İlişkili ManyToManyField temizleme
        self.txID = ""

        self.save()  # Tüm değişiklikleri kaydet

    def __str__(self):
        return self.email if self.email else "Unnamed Item"  # Eğer isim boşsa varsayılan bir değer döndür

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    @staticmethod
    def generate_random_password(length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

class pointGroup(models.Model):
    one = models.OneToOneField(ArchivedItem, on_delete=models.CASCADE, related_name='group_one', null=True)
    two = models.OneToOneField(ArchivedItem, on_delete=models.CASCADE, related_name='group_two', null=True)
    three = models.OneToOneField(ArchivedItem, on_delete=models.CASCADE, related_name='group_three', null=True)
    four = models.OneToOneField(ArchivedItem, on_delete=models.CASCADE, related_name='group_four', null=True)
    five = models.OneToOneField(ArchivedItem, on_delete=models.CASCADE, related_name='group_five', null=True)
    six = models.OneToOneField(ArchivedItem, on_delete=models.CASCADE, related_name='group_six', null=True)
    seven = models.OneToOneField(ArchivedItem, on_delete=models.CASCADE, related_name='group_seven', null=True)
    eight = models.OneToOneField(ArchivedItem, on_delete=models.CASCADE, related_name='group_eight', null=True)
    nine = models.OneToOneField(ArchivedItem, on_delete=models.CASCADE, related_name='group_nine', null=True)
    table_business = models.ForeignKey('tableBusiness', related_name='blocks', on_delete=models.CASCADE)
    
    def clean(self):
        max_groups = 11
        if pointGroup.objects.filter(table_business=self.table_business).count() >= max_groups:
            raise ValidationError(f"Each tableBusiness can have at most {max_groups} pointGroups.")
        
class tableBusiness(models.Model):
    businessLine = models.OneToOneField(BusinessLine, on_delete=models.CASCADE)