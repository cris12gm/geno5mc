from django import forms
from django.core.validators import RegexValidator
from querySNP.models import SNPinfo

my_validator = RegexValidator(r"rs", "The snpID should be in this format: rs87894568")
class QuerySNP(forms.Form):
    SNPid = forms.CharField(label='SNP id:',max_length=15, validators=[my_validator], widget=forms.TextInput(
        attrs={'placeholder':'Introduce SNPid',}))