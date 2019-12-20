from django.db import models
from django import forms
    
class Geneinfo(models.Model):
    geneID = forms.CharField(help_text="Enter a Gene id.")
