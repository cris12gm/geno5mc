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
import requests

from queryGene.plotExpression import plotExpression
from queryGene.plotElements import plotTrafficLights, plotPromoter

from .forms import QueryGene
from .models import snpsAssociated_FDR_promotersEPD, snpsAssociated_FDR_chrom, getGeneID, snpsAssociated_FDR_enhancers, snpsAssociated_FDR_trafficLights, getGencode,genes,topResultsGenes,getMethylation,getAllPromoters

class Errors(Enum):
    NO_ERROR = 0
    NOT_VALID = 1
    NOT_ASSOCIATED = 2

def queryMore(request):
    dataOut = {}
    dataIn = request.GET.get('snps', None).replace("buttonSNP_","").replace("buttonSNP-TL_","").replace(";",", ")
    dataOut["snps"] = dataIn
    dataOut["cpg"] = "SNPs associated with "+request.GET.get('chrom',None)+":"+str(request.GET.get('cpg',None))
    return JsonResponse(dataOut)

def queryExpression(request):
    dataGen = {}
    geneCode = request.GET.get('geneCode', None).replace("buttonGTEx","")
    expression = requests.get("https://gtexportal.org/rest/v1/expression/geneExpression?datasetId=gtex_v7&gencodeId="+geneCode+"&format=json").json()['geneExpression']    
    gTEX = plotExpression(expression)

    dataGen["plot"]=gTEX

    return JsonResponse(dataGen)

def queryPlotPromoter(request):
    dataPlot = {}

    promoterID = request.GET.get('promoterVal', None)
    snpID = request.GET.get('snpID', None)
    if promoterID:
        plot,coordinates = plotPromoter(promoterID,snpID)
        dataPlot['plot']="<center>"+plot+"</center>"
        dataPlot['coordinates'] = coordinates
    else:
        dataPlot['plot']=""

    return JsonResponse(dataPlot)

def queryPlotTLights(request):
    dataPlot = {}

    snpID = request.GET.get('snpID', None)
    geneID = request.GET.get('geneID', None)
    if snpID:
        plot = plotTrafficLights(snpID,geneID)
        dataPlot['plot'] = "<center>"+plot+"</center>"
    else:
        dataPlot['plot'] = ""
    return JsonResponse(dataPlot)

class GenesAssociated(TemplateView):
    template = 'queryGene.html'

    def get(self, request): 

        return redirect(settings.SUB_SITE+"/query/#gene")

    def post(self, request):

        form = QueryGene(request.POST)
        error = None
        similarV = []

        baseLink = settings.SUB_SITE

        # Variables gene 
        geneCode = ""
        description = ""
        chrom = ""

        #Variables promoters
        promotersOut = {}
        promoters = []
        promoterIDs = []
        allPromoters = []
        countPromoters = ""
        countPromotersAssociated = ""

        tLights = {}
        countTLights = ""

        if form.is_valid():
            geneId = form.cleaned_data.get('GeneId')

            #GET GENCODE
            try:
                geneCode = getGencode.getGencodeID(geneId)
            except:
                pass

            #GET PROMOTERS

            prePromoterIDs = snpsAssociated_FDR_promotersEPD.getPromoterIDs(geneId)
            promoterIDs = {}
            if prePromoterIDs:
                for element in prePromoterIDs:
                    try:
                        value = promoterIDs[element.promoterID]
                    except:
                        value = []
                    value.append(element.snpID)
                    promoterIDs[element.promoterID] = value
                countPromotersAssociated = len(promoterIDs)
            
                promoters = snpsAssociated_FDR_promotersEPD.get_SNPs_Promoters(geneId)

                ##GET ALL PROMOTERS
                allPromoters = getAllPromoters.getAllPromoters_Gene(geneId)
                newAllPromoters = []
                if allPromoters:
                    for promoter in allPromoters:
                        try:
                            promoterIDs[promoter.id]
                            setattr(promoter, 'associated', True)
                        except:
                            setattr(promoter, 'associated', False)
                        newAllPromoters.append(promoter)
                    allPromoters = newAllPromoters
                    countPromoters = len(allPromoters)  
            
            ##Proceso promotores
            if promoters:
                for element in promoters:
                    chrom = element.chrom
                    cpg = element.chromStartCpG
                    snpID = element.snpID
                    promoterID = element.promoterID
                    try:
                        [snps,allsnps,button] = promotersOut[promoterID,cpg]
                        if button<5:
                            snps = snps+", "+snpID
                        allsnps = allsnps + ";"+ element.snpID                    
                        button = button + 1
                    except:
                        snps = snpID
                        allsnps = snpID
                        button = 1

                    promotersOut[promoterID,cpg] = [snps,allsnps,button]

            
            ##GET TLIGHTS
            pretLights = snpsAssociated_FDR_trafficLights.get_trafficLights(geneId)
            snps_select = {}
            if pretLights:
                for element in pretLights:
                    chrom = element.chrom
                    cpg = str(element.chromStartTL)
                    snpID = element.snpID
                    try:
                        [snps,allsnps,button] = tLights[cpg]
                        if button<5:
                            snps = snps+", "+snpID
                        allsnps = allsnps + ";" + element.snpID
                        button = button + 1
                    except:
                        snps = snpID
                        allsnps = snpID
                        button = 1
                    snps_select[snpID] = ""
                    tLights[cpg] = [snps,allsnps,button]
                countTLights = len(tLights)




            if promoters is None and tLights==None:
                geneInDB = getGeneID.get_Genes(geneId)
                if geneInDB!=None:
                    error = Errors.NOT_ASSOCIATED
                else:
                    error = Errors.NOT_VALID
                
                    ##Si no es válido, busco similares
                    if "*" in geneId:
                        similar = getGeneID.getSimilar(geneId.replace("*","%"))
                    else:
                        similar = getGeneID.getSimilar("%"+geneId+"%")
                        try:
                            for i in range(0,len(geneId)):
                                groupL = geneId[i]+geneId[i+1]+geneId[i+2]
                                try:
                                    similarG = getGeneID.getSimilar("%"+groupL+"%")
                                    for element in similarG:
                                        similar.append(element)
                                except:
                                    continue
                        except:
                            pass
                    if len(similar)>20:
                        similar = getGeneID.getSimilar(geneId+"%")

                    if len(similar)>0 and len(similar)<30:
                        for element in similar:
                            similarV.append(getattr(element,"geneID"))
                        similarV = set(similarV)
                    else:
                        similarV = "tooLong"
            else:
                try:
                    description = getattr(genes.get_geneDescription(geneId),"description")
                except:
                    description = ""
        else:
            error = Errors.NOT_VALID
            ##Si no es válido, busco similares

            if "*" in geneId:
                similar = getGeneID.getSimilar(geneId.replace("*","%"))
            else:
                similar = getGeneID.getSimilar("%"+geneId+"%")
                try:
                    for i in range(0,len(geneId)):
                        groupL = geneId[i]+geneId[i+1]+geneId[i+2]
                        try:
                            similarG = getGeneID.getSimilar("%"+groupL+"%")
                            similar.append(similarG)
                        except:
                            continue
                except:
                    pass
                if len(similar)>20:
                    similar = getGeneID.getSimilar(geneId+"%")

                if len(similar)>0 and len(similar)<30:
                    for element in similar:
                        similarV.append(getattr(element,"geneID"))
                        similarV = set(similarV)
                else:
                    similarV = "tooLong"
        return render(request, self.template, {
            'geneId': geneId,
            'geneCode': geneCode,
            'chrom':chrom,
            'promoterIDs':promoterIDs,
            'allPromoters':allPromoters,
            'countPromoters':countPromoters,
            'countPromotersAssociated':countPromotersAssociated,
            'promoters': promotersOut,
            'tLights': tLights,
            'countTLights':countTLights,
            'snpsSelect':snps_select,
            'description':description,
            'baseLink': baseLink,
            'error': error,
            'similar':similarV
        })   

class GenesAssociatedGET(TemplateView):
    template = 'queryGene.html'

    def get(self, request, gene):

        error = None
        similarV = []

        baseLink = settings.SUB_SITE

        # Variables gene 
        geneCode = ""
        description = ""

        #Variables promoters
        promotersOut = {}
        promoters = []
        promoterIDs = []
        allPromoters = []
        countPromoters = ""
        countPromotersAssociated = ""

        tLights = {}
        countTLights = ""

        geneId = gene 

        #GET GENCODE
        try:
            geneCode = getGencode.getGencodeID(geneId)
        except:
            pass

        #GET PROMOTERS

        prePromoterIDs = snpsAssociated_FDR_promotersEPD.getPromoterIDs(geneId)
        promoterIDs = {}
        if prePromoterIDs:
            for element in prePromoterIDs:
                try:
                    value = promoterIDs[element.promoterID]
                except:
                    value = []
                value.append(element.snpID)
                promoterIDs[element.promoterID] = value
            countPromotersAssociated = len(promoterIDs)
        
            promoters = snpsAssociated_FDR_promotersEPD.get_SNPs_Promoters(geneId)

            ##GET ALL PROMOTERS
            allPromoters = getAllPromoters.getAllPromoters_Gene(geneId)
            newAllPromoters = []
            if allPromoters:
                for promoter in allPromoters:
                    try:
                        promoterIDs[promoter.id]
                        setattr(promoter, 'associated', True)
                    except:
                        setattr(promoter, 'associated', False)
                    newAllPromoters.append(promoter)
                allPromoters = newAllPromoters
                countPromoters = len(allPromoters)  
            
            ##Proceso promotores
            if promoters:
                promotersOut = {}
                for element in promoters:
                    cpg = element.chromStartCpG
                    snpID = element.snpID
                    promoterID = element.promoterID
                    try:
                        snps = promotersOut[promoterID,cpg]
                        snps = snps+", "+snpID
                    except:
                        snps = snpID
                    
                    promotersOut[promoterID,cpg] = snps

    ##GET TLIGHTS
        pretLights = snpsAssociated_FDR_trafficLights.get_trafficLights(geneId)
        if pretLights:
            for element in pretLights:
                chrom = element.chrom
                cpg = str(element.chromStartTL)
                snpID = element.snpID
                try:
                    [snps,allsnps,button] = tLights[cpg]
                    if button<5:
                        snps = snps+", "+snpID
                    allsnps = allsnps + ";" + element.snpID
                    button = button + 1
                except:
                    snps = snpID
                    allsnps = snpID
                    button = 1
                tLights[cpg] = [snps,allsnps,button]
            countTLights = len(tLights)

        if promoters is None and tLights==None:
            geneInDB = getGeneID.get_Genes(geneId)
            if geneInDB!=None:
                error = Errors.NOT_ASSOCIATED
            else:
                error = Errors.NOT_VALID
            
                ##Si no es válido, busco similares
                if "*" in geneId:
                    similar = getGeneID.getSimilar(geneId.replace("*","%"))
                else:
                    similar = getGeneID.getSimilar("%"+geneId+"%")
                    try:
                        for i in range(0,len(geneId)):
                            groupL = geneId[i]+geneId[i+1]+geneId[i+2]
                            try:
                                similarG = getGeneID.getSimilar("%"+groupL+"%")
                                for element in similarG:
                                    similar.append(element)
                            except:
                                continue
                    except:
                        pass
                if len(similar)>20:
                    similar = getGeneID.getSimilar(geneId+"%")

                if len(similar)>0 and len(similar)<30:
                    for element in similar:
                        similarV.append(getattr(element,"geneID"))
                    similarV = set(similarV)
                else:
                    similarV = "tooLong"
        else:
            try:
                description = getattr(genes.get_geneDescription(geneId),"description")
            except:
                description = ""
        
        return render(request, self.template, {
            'geneId': geneId,
            'geneCode': geneCode,
            'chrom':chrom,
            'promoterIDs':promoterIDs,
            'allPromoters':allPromoters,
            'countPromoters':countPromoters,
            'countPromotersAssociated':countPromotersAssociated,
            'promoters': promotersOut,
            'tLights': tLights,
            'countTLights':countTLights,
            'description':description,
            'baseLink': baseLink,
            'error': error,
            'similar':similarV
        })   