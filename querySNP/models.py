from django.db import models
from django import forms
    
class SNPinfo(models.Model):
    snpID = forms.CharField(help_text="Enter an SNP id.")