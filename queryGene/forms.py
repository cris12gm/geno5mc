from django import forms
from querySNP.models import SNPinfo

class QueryGene(forms.Form):
    Geneid = forms.CharField(label='Gene id:',max_length=15, widget=forms.TextInput(
        attrs={'placeholder':'Introduce Geneid',}))