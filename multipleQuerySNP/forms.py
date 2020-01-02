from django import forms
from django.core.validators import RegexValidator

class MultipleQuerySNP(forms.Form):
    SNPids = forms.CharField(label="",initial="rs2845392\nrs10740756", widget=forms.Textarea(attrs={'cols': '15','rows':'5'}))
