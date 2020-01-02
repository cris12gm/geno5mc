from django import forms
# from querySNP.models import SNPinfo

class QueryGene(forms.Form):
    GeneId = forms.CharField(label='Gene id: (eg:ACR)',max_length=15, initial='ACR', widget=forms.TextInput(
        attrs={'placeholder':'Introduce Gene Id',}))