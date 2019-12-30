from django import forms
from django.core.validators import RegexValidator

my_validator = RegexValidator(r"rs[0-9]{1,15}", "The snpID should be in this format: rs87894568")
class MultipleQuerySNP(forms.Form):
    SNPid = forms.CharField(label='SNP id:',max_length=15, validators=[my_validator], initial="rs2845392", widget=forms.TextInput(
        attrs={'placeholder':'Introduce SNPid',}))
