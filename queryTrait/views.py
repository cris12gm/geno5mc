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

from .models import PhenotypeGenotype,PhenotypeGenotypeFDR,snpsAssociated_FDR_promotersEPD,snpsAssociated_FDR_chrom

class TraitsAssociated(TemplateView):
    template = 'queryTrait.html'
    
    
    def get(self, request):  
        baseLink = settings.SUB_SITE+"/querySNP/snp/"
        #Get all traits and pass to form 
        traits = PhenotypeGenotypeFDR.get_All_Traits()
        traitsList = []

        for element in traits:
            trait = getattr(element,"trait")
            traitsList.append(trait)
        return render(request, self.template, {
            'traits':traitsList
        })

    def post (self, request):
        baseLink = settings.SUB_SITE+"/querySNP/snp/"
        selectedTrait = request.POST['traitslist']
        snpsTrait = PhenotypeGenotypeFDR.get_All_SNP_Trait(selectedTrait)
        snpsOut = []
        for snp in snpsTrait:
            snpInfo = snpsAssociated_FDR_chrom.get_SNP_info(getattr(snp,"snpID"))
            snpsOut.append(snpInfo)      
        #for snp in snpsTrait:
        #    promoters = snpsAssociated_FDR_promotersEPD.get_Promoters(getattr(snp,"snpID"))
        return render(request, self.template, {
            'selectedTrait':selectedTrait,
            'snpsOut':snpsOut,
            'baseLink':baseLink
        })