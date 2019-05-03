from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import pandas as pd
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    
    #Additional Features
    profile_pic = models.ImageField(default='default.jpg',upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def save(self):
        super().save()
        img = Image.open(self.profile_pic.path)
        
        if img.height>300 or img.width>300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

class GWL_inputs(models.Model):
    import os
    
    current_directory = os.getcwd()+'\\basic_app\\website_data_20190225.csv'
    current_directory = current_directory.replace('\\','/')
    ori = pd.read_csv(current_directory)

    dataset = ori['STATE'].unique()
    choices0 = []
    for i in range(0,dataset.shape[0]):
        choices0.append([dataset[i],dataset[i]])
    state = models.CharField(max_length=9, choices=choices0, default='State')

    dataset = ori['DISTRICT'].unique()
    choices1 = []
    for i in range(0,dataset.shape[0]):
        choices1.append([dataset[i],dataset[i]])
    district = models.CharField(max_length=9, choices=choices1, default='District')

    dataset = ori['BLOCK_NAME'].unique()
    choices2 = []
    for i in range(0,dataset.shape[0]):
        choices2.append([dataset[i],dataset[i]])
    block = models.CharField(max_length=9, choices=choices2, default='Block_Name', primary_key=True)

    def __str__(self):
        return self.block

class Site_Name(models.Model):
    block = models.ForeignKey(GWL_inputs, on_delete=models.CASCADE)
    site = models.CharField(max_length=15, choices=[['---','---'],], default='---')
    # site = forms.Select(choices=['---']) Choices

    def __str__(self):
        return self.site

class FYear (models.Model):
    year = models.IntegerField(validators=[MinValueValidator(2016), MaxValueValidator(2025)], default=datetime.date.today().year)

    def __str__(self):
        return self.year

class City(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
