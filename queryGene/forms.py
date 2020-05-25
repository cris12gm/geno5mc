from django import forms
from .models import snpsAssociated_FDR_promotersEPD
# from querySNP.models import SNPinfo

class QueryGene(forms.Form):
    GeneId = forms.CharField(label='Gene ID:',max_length=15, widget=forms.TextInput())