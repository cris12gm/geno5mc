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

from datetime import datetime
import csv
from sqlalchemy import inspect

from .forms import QuerySNP
from .models import snpsAssociated_FDR_chrom, snpsAssociated_FDR_chr_table, snpsAssociated_FDR_promotersEPD, snpsAssociated_FDR_enhancers, snpsAssociated_FDR_trafficLights,getSNPID,topResults,genes,enhancers,PhenotypeGenotypeFDR
from querySNP.plotElements import plotPromoters, plotEnhancers, plotTrafficLights

class Errors(Enum):
    NO_ERROR = 0
    NOT_VALID = 1
    NOT_ASSOCIATED = 2

def getAllFromSNP(snpId,associations,promoters,enhancers,tLights,topResultPromoter,topResultEnhancer,snpInfo,linkFileAssociations,traits,error):
    snpInfo = snpsAssociated_FDR_chrom.get_SNP_chrom(snpId)
    if snpInfo is None:
        checkid = getSNPID.get_SNP(snpId)
        if checkid!=None:
            error = Errors.NOT_ASSOCIATED
            snpInfo = {}
            snpInfo["snpID"] = snpId
        else:
            error = Errors.NOT_VALID
    else:
        associations = snpsAssociated_FDR_chr_table(snpInfo.chrom).get_Associated(snpInfo.snpID)

        #Save associations to file
        
        fileNameAssociations = settings.MEDIA_ROOT+str(datetime.now()).split(".")[0].replace(" ","_").replace(":","_")+"_"+snpId+".txt"
        f = open(fileNameAssociations,'w')
        header = "chrom\tchromStart\tsnpID\tchromStartSNP\trefBase\taltBase\theteroBase\tuRefBase\tuAltBase\tuHeteroBase\tiRefBase\tiAltBase\tother\tmethCount\tnumSamples\tpValue\tqValue\n"
        f.write(header)

        for element in associations:
            inst = inspect(element)
            attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
            line = ""
            for att in attr_names:
                line = line+str(getattr(element,att))+"\t"
            line = (line+"\n").replace("\t\n","\n")
            f.write(line)
        f.close()

        linkFileAssociations = fileNameAssociations.replace(settings.MEDIA_ROOT,settings.MEDIA_URL)

        promoters = snpsAssociated_FDR_promotersEPD.get_Promoters(snpId)
        # Añado a promoters el count
        if promoters:
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

        #Get Top Results

        #topResult = topResults.get_TopResults(snpInfo.snpID)

        topResultPromoter = topResults.get_TopElement(snpInfo.snpID,"Promoter")
        topResultEnhancer = topResults.get_TopElement(snpInfo.snpID,"Enhancer")

        traits = PhenotypeGenotypeFDR.get_SNP_Trait(snpInfo.snpID)
        
    return snpInfo,associations,promoters,enhancers,tLights,topResultPromoter,topResultEnhancer,linkFileAssociations,traits,error

def queryGeneDescription(request):
    templateError = "error.html"
    try:
        geneID = request.GET.get('geneID', None).replace("buttonPromoters","")
        description = getattr(genes.get_geneDescription(geneID),"description")

        dataGen = {}
        dataGen["geneID"]=geneID
        dataGen["geneDescription"]=description

        return JsonResponse(dataGen)
    except:
        return render(request, templateError)
def queryEnhancerDescription(request):
    templateError = "error.html"
    try:
        enhancerID = request.GET.get('name', None).replace("buttonEnhancers","")
        description = getattr(enhancers.get_enhancerData(enhancerID),"genes").replace(";",", ")

        dataGen = {}
        dataGen["enhancerID"]="Genes regulated by: "+enhancerID
        dataGen["enhancerGenes"]=description
        return JsonResponse(dataGen)
    except:
        return render(request, templateError)

class SNPAssociated(TemplateView):
    template = 'querySNP.html'    

    def get(self, request): 

        return redirect(settings.SUB_SITE+"/query/#snp")

    def post(self, request):
        form = QuerySNP(request.POST)
        baseLink = settings.SUB_SITE
        error = None
        snpInfo = {}
        associations = []
        promoters = []
        enhancers = []
        tLights=[]
        topResultPromoter = []
        topResultEnhancer = []
        linkFileAssociations = ""
        barPlotPromoters = []
        barPlotEnhancers = []
        barPlotTLights = []
        traits = ""
        error = ""

        if form.is_valid():
            snpId = form.cleaned_data.get('SNPid')
            if snpId is not '':
                snpInfo,associations,promoters,enhancers,tLights,topResultPromoter,topResultEnhancer,linkFileAssociations,traits,error=getAllFromSNP(snpId,associations,promoters,enhancers,tLights,topResultPromoter,topResultEnhancer,snpInfo,linkFileAssociations,traits,error)
                if promoters:
                    barPlotPromoters = plotPromoters(promoters)
                if enhancers:
                    barPlotEnhancers = plotEnhancers(enhancers)
                if tLights:
                    barPlotTLights = plotTrafficLights(tLights)
                    
        else:
            error = Errors.NOT_VALID

        return render(request, self.template, {
            'snpInfo': snpInfo,
            'traits':traits,
            'associations': associations,
            'promoters': promoters,
            'enhancers':enhancers,
            'tLights':tLights,
            'topResultPromoter':topResultPromoter,
            'topResultEnhancer':topResultEnhancer,
            'query_form': form,
            'baseLink':baseLink,
            'linkFileAssociations':linkFileAssociations,
            'barPlotPromoters':barPlotPromoters,
            'barPlotEnhancers':barPlotEnhancers,
            'barPlotTLights':barPlotTLights,
            'error': error
        })   

class SNPAssociatedGET(TemplateView):

    template = 'querySNP.html'
        
    def get(self, request, snp):

        snpId = snp
        form = QuerySNP()
        baseLink = settings.SUB_SITE
        error = None
        snpInfo = {}
        associations = []
        promoters = []
        enhancers = []
        tLights=[]
        topResultPromoter = []
        topResultEnhancer = []
        linkFileAssociations = ""
        barPlotPromoters = []
        barPlotEnhancers = []
        barPlotTLights = []
        traits = ""
        error = ""

        if snpId is not '':
            snpInfo,associations,promoters,enhancers,tLights,topResultPromoter,topResultEnhancer,linkFileAssociations,traits,error=getAllFromSNP(snpId,associations,promoters,enhancers,tLights,topResultPromoter,topResultEnhancer,snpInfo,linkFileAssociations,traits,error)
            if promoters:
                barPlotPromoters = plotPromoters(promoters)
            if enhancers:
                barPlotEnhancers = plotEnhancers(enhancers)
            if tLights:
                barPlotTLights = plotTrafficLights(tLights)
                    
        else:
            error = Errors.NOT_VALID

        return render(request, self.template, {
            'snpInfo': snpInfo,
            'traits':traits,
            'associations': associations,
            'promoters': promoters,
            'enhancers':enhancers,
            'tLights':tLights,
            'topResultPromoter':topResultPromoter,
            'topResultEnhancer':topResultEnhancer,
            'query_form': form,
            'baseLink':baseLink,
            'linkFileAssociations':linkFileAssociations,
            'barPlotPromoters':barPlotPromoters,
            'barPlotEnhancers':barPlotEnhancers,
            'barPlotTLights':barPlotTLights,
            'error': error
        })   

class SNPAssociatedTour(TemplateView):
    template = 'tour/tour_2.html'
        
    def get(self, request):

        snpId = "rs727563"
        baseLink = settings.SUB_SITE
        snpInfo = {}
        associations = []
        promoters = []
        enhancers = []
        tLights=[]
        topResultPromoter = []
        topResultEnhancer = []
        linkFileAssociations = ""
        barPlotPromoters = []
        barPlotEnhancers = []
        barPlotTLights = []
        traits = ""
        error = ""

        if snpId is not '':
            snpInfo,associations,promoters,enhancers,tLights,topResultPromoter,topResultEnhancer,linkFileAssociations,traits,error=getAllFromSNP(snpId,associations,promoters,enhancers,tLights,topResultPromoter,topResultEnhancer,snpInfo,linkFileAssociations,traits,error)
            if promoters:
                barPlotPromoters = plotPromoters(promoters)
            if enhancers:
                barPlotEnhancers = plotEnhancers(enhancers)
            if tLights:
                barPlotTLights = plotTrafficLights(tLights)
                    

        return render(request, self.template, {
            'snpInfo': snpInfo,
            'traits':traits,
            'associations': associations,
            'promoters': promoters,
            'enhancers':enhancers,
            'tLights':tLights,
            'topResultPromoter':topResultPromoter,
            'topResultEnhancer':topResultEnhancer,
            'baseLink':baseLink,
            'linkFileAssociations':linkFileAssociations,
            'barPlotPromoters':barPlotPromoters,
            'barPlotEnhancers':barPlotEnhancers,
            'barPlotTLights':barPlotTLights,
        })   

class SNPAssociatedTour_4(TemplateView):
    template = 'tour/tour_4.html'
        
    def get(self, request):

        snpId = "rs727563"
        baseLink = settings.SUB_SITE
        snpInfo = {}
        associations = []
        promoters = []
        enhancers = []
        tLights=[]
        topResultPromoter = []
        topResultEnhancer = []
        linkFileAssociations = ""
        barPlotPromoters = []
        barPlotEnhancers = []
        barPlotTLights = []
        traits = ""
        error = ""

        if snpId is not '':
            snpInfo,associations,promoters,enhancers,tLights,topResultPromoter,topResultEnhancer,linkFileAssociations,traits,error=getAllFromSNP(snpId,associations,promoters,enhancers,tLights,topResultPromoter,topResultEnhancer,snpInfo,linkFileAssociations,traits,error)
            if promoters:
                barPlotPromoters = plotPromoters(promoters)
            if enhancers:
                barPlotEnhancers = plotEnhancers(enhancers)
            if tLights:
                barPlotTLights = plotTrafficLights(tLights)
                    

        return render(request, self.template, {
            'snpInfo': snpInfo,
            'traits':traits,
            'associations': associations,
            'promoters': promoters,
            'enhancers':enhancers,
            'tLights':tLights,
            'topResultPromoter':topResultPromoter,
            'topResultEnhancer':topResultEnhancer,
            'baseLink':baseLink,
            'linkFileAssociations':linkFileAssociations,
            'barPlotPromoters':barPlotPromoters,
            'barPlotEnhancers':barPlotEnhancers,
            'barPlotTLights':barPlotTLights,
        })   