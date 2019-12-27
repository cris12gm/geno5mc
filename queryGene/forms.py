from django import forms
# from querySNP.models import SNPinfo

class QueryGene(forms.Form):
    GeneId = forms.CharField(label='Gene id:',max_length=15, initial='POTEE', widget=forms.TextInput(
        attrs={'placeholder':'Introduce Gene Id',}))