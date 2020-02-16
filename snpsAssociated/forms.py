from django import forms
from django.core.validators import RegexValidator

my_validator = RegexValidator(r"rs[0-9]{1,15}", "The snpID should be in this format: rs727563")

class QuerySNP(forms.Form):
    SNPid = forms.CharField(max_length=15, validators=[my_validator], initial="rs727563", widget=forms.TextInput(
        attrs={'placeholder':'Introduce SNPid',}))

class QueryGene(forms.Form):
    GeneId = forms.CharField(label='Gene id: (eg:ACR)',max_length=15, initial='ACR', widget=forms.TextInput(
        attrs={'placeholder':'Introduce Gene Id',}))
