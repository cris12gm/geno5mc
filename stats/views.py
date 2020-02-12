import itertools
from django.conf import settings
import datetime
import os
from enum import Enum
from functools import reduce
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import FormView, DetailView, TemplateView
from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import snpsAssociated_FDR_chrom
# Create your views here.

class stats(TemplateView):
    template = "stats.html"

    def post(self,request):
        pass
        return render(request, self.template, {})
    def get(self,request):
        #Get number of snpsAssociated
        numAssociatedSNP = snpsAssociated_FDR_chrom.get_SNP_chrom()[0]
        
        
        return render(request, self.template, {
            'numAssociatedSNP':numAssociatedSNP
        })

