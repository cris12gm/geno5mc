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

from .models import snpsAssociated_FDR_chr_table
from queryRegion.plotMethylation import plotRegion

class Errors(Enum):
    NO_ERROR = 0
    VERY_LONG = 1
    START_END = 2

def queryViewMore(request):

    dataOut = {}
    dataIn = request.GET.get('snps', None).replace("buttonSNP_","").replace(";",", ")
    dataOut["snps"]=dataIn

    return JsonResponse(dataOut)

def queryPlotMeth(request):
    dataOut = {}

    region = request.GET.get('region',None).replace("buttonPlot","").replace(" ","-")
    associated = eval(request.GET.get('associated',None))
    plot = plotRegion(region,associated)

    dataOut['plot']="<center>"+plot+"</center>"
    return JsonResponse(dataOut)

class RegionAssociated(TemplateView):
    template = 'queryRegion.html'

    def get(self, request): 

        return redirect(settings.SUB_SITE+"/query/#region")

    def post(self, request):
        
        region = ""
        cpgs = []
        error = ""
        associations = {}

        chrom = request.POST['chrom'].split("_")[0]
        chromStart = request.POST['chromStart']
        chromEnd = request.POST['chromEnd']

        length = abs(int(chromEnd) - int(chromStart))
        region = chrom+" "+chromStart+"-"+chromEnd
        ###Check length

        if length>1000:
            error = Errors.VERY_LONG
        elif int(chromEnd)<int(chromStart):
            error = Errors.START_END
        else:
            ##Get associations
            associationsRaw = snpsAssociated_FDR_chr_table(chrom).get_Associated_Region(chromStart,chromEnd)
            for element in associationsRaw:
                cpg = element.chromStart
                cpgs.append(cpg)
                try:
                    snps,allsnps,button = associations[cpg]
                     
                    if button<5:
                        snps = snps+", "+element.snpID
                    button = button + 1 
                    allsnps = allsnps + ";"+element.snpID
                    
                except:
                    snps = element.snpID
                    allsnps = element.snpID
                    button = 1
                associations[cpg] = snps,allsnps,button
            cpgs = set(cpgs)
        return render(request, self.template, {
            'region':region,
            'associations':associations,
            'cpgs':cpgs,
            'error':error
        })   
