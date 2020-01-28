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

from .forms import QuerySNP
from .models import snpsAssociated_FDR_chrom, snpsAssociated_FDR_chr_table, snpsAssociated_FDR_promotersEPD, snpsAssociated_FDR_enhancers, snpsAssociated_FDR_trafficLights,getSNPID
from querySNP.plotElements import plotPromoters

class Errors(Enum):
    NO_ERROR = 0
    NOT_VALID = 1
    NOT_ASSOCIATED = 2

def getAllFromSNP(snpId,associations,promoters,enhancers,tLights,snpInfo,error):
    snpInfo = snpsAssociated_FDR_chrom.get_SNP_chrom(snpId)
    if snpInfo is None:
        checkid = getSNPID.get_SNP(snpId)
        if checkid!=None:
            error = Errors.NOT_ASSOCIATED
        else:
            error = Errors.NOT_VALID
    else:
        associations = snpsAssociated_FDR_chr_table(snpInfo.chrom).get_Associated(snpInfo.snpID)
        promoters = snpsAssociated_FDR_promotersEPD.get_Promoters(snpId)
        # Añado a promoters el count
        promotersNew = []
        for gene in promoters:
            info = {
                'data': gene[1],
                'link': settings.SUB_SITE+"/queryGene/gene/"+gene[1].geneID,
                'count': gene[0],
                'distance':abs(gene[1].chromStartPromoter-snpInfo.chromStart)
            }
            promotersNew.append(info)
        promoters = promotersNew

        enhancers = snpsAssociated_FDR_enhancers.get_Enhancers(snpId)

        #Añado a tlights el count
        tLights = snpsAssociated_FDR_trafficLights.get_trafficLights(snpInfo.snpID)
    return snpInfo,associations,promoters,enhancers,tLights,error

class SNPAssociated(TemplateView):
    template = 'querySNP.html'    

    def get(self, request):  
        form = QuerySNP()
        return render(request, self.template, {
            'query_form': form
        })

    def post(self, request):
        form = QuerySNP(request.POST)
        baseLink = settings.SUB_SITE+"/queryGene/gene/"
        error = None
        snpInfo = {}
        associations = []
        promoters = []
        enhancers = []
        tLights=[]
        error = ""

        if form.is_valid():
            snpId = form.cleaned_data.get('SNPid')
            if snpId is not '':
                snpInfo,associations,promoters,enhancers,tLights,error=getAllFromSNP(snpId,associations,promoters,enhancers,tLights,snpInfo,error)
                inputDict = {}
                inputDict['test1']=10
                inputDict['test2']=20
                barPlotPromoters = plotPromoters(promoters)
                barPlotPromoters2 = plotPromoters(promoters)
        else:
            error = Errors.NOT_VALID

        return render(request, self.template, {
            'snpInfo': snpInfo,
            'associations': associations,
            'promoters': promoters,
            'enhancers':enhancers,
            'tLights':tLights,
            'query_form': form,
            'baseLink':baseLink,
            'error': error,
            'barPlotPromoters':barPlotPromoters,
            'barPlotPromoters2':barPlotPromoters2
        })   

class SNPAssociatedGET(TemplateView):
    template = 'querySNPWF.html'
        

    def get(self, request, snp):

        form = QuerySNP()
        error = None
        snpInfo = {}
        baseLink = settings.SUB_SITE+"/queryGene/gene/" 
        associations = []
        promoters = []
        enhancers = []
        tLights=[]

        snpId = snp
        if snpId is not '':
            snpInfo,associations,promoters,enhancers,tLights,error=getAllFromSNP(snpId,associations,promoters,enhancers,tLights,snpInfo,error)
        else:
            error = Errors.NOT_VALID


        return render(request, self.template, {
            'snpInfo': snpInfo,
            'associations': associations,
            'promoters': promoters,
            'enhancers':enhancers,
            'tLights':tLights,
            'query_form': form,
            'baseLink':baseLink,
            'error': error
        })   