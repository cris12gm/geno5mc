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
from queryGene.plotElements import plotPromoters, plotEnhancers, plotTrafficLights

from .forms import QueryGene
from .models import snpsAssociated_FDR_promotersEPD, snpsAssociated_FDR_chrom, getGeneID, snpsAssociated_FDR_enhancers, snpsAssociated_FDR_trafficLights, getGencode,genes

class Errors(Enum):
    NO_ERROR = 0
    NOT_VALID = 1
    NOT_ASSOCIATED = 2

def queryExpression(request):
    dataGen = {}
    geneCode = request.GET.get('geneCode', None).replace("buttonGTEx","")
    expression = requests.get("https://gtexportal.org/rest/v1/expression/geneExpression?datasetId=gtex_v7&gencodeId="+geneCode+"&format=json").json()['geneExpression']    
    gTEX = plotExpression(expression)

    dataGen["plot"]=gTEX

    return JsonResponse(dataGen)

class GenesAssociated(TemplateView):
    template = 'queryGene.html'

    def get(self, request): 

        return redirect(settings.SUB_SITE+"/query/#gene")

    def post(self, request):
        form = QueryGene(request.POST)
        error = None
        similar = ""

        baseLink = settings.SUB_SITE

        promoters = []
        enhancers = []
        tLights = []
        barPlotPromoters = ""
        barPlotEnhancers = ""
        barPlotTLights = ""
        geneCode = ""
        description = ""

        if form.is_valid():
            geneId = form.cleaned_data.get('GeneId')
            try:
                geneCode = getGencode.getGencodeID(geneId)
            except:
                pass
            #GET PROMOTERS
            promoters = snpsAssociated_FDR_promotersEPD.get_SNPs_Promoters(geneId)
            if promoters:
                barPlotPromoters = plotPromoters(promoters)

            ##GET ENHANCERS
            enhancers = snpsAssociated_FDR_enhancers.get_Enhancers(geneId)
            if enhancers:
                barPlotEnhancers = plotEnhancers(enhancers)

            ##GET TLIGHTS
            tLights = snpsAssociated_FDR_trafficLights.get_trafficLights(geneId)
            if tLights:
                barPlotTLights = plotTrafficLights(tLights)
            
            if geneId is not '':
                if promoters is None and enhancers==None and tLights==None:
                    geneInDB = getGeneID.get_Genes(geneId)
                    if geneInDB!=None:
                        error = Errors.NOT_ASSOCIATED
                    else:
                        error = Errors.NOT_VALID
                        ##Si no es válido, busco similares
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
                            similar = "tooLong"
                else:
                    # Añado a genes el count
                    if promoters is not None:
                        promotersAssociatedNew = []
                        for gene in promoters:
                            chromStart = snpsAssociated_FDR_chrom.get_SNP_chrom(gene[1].snpID).chromStart
                            info = {
                                'data': gene[1],
                                'count': gene[0],
                                'link': settings.SUB_SITE+"/querySNP/snp/"+gene[1].snpID,
                                'distance': abs((gene[1].chromStartPromoter)-(chromStart))
                            }
                            promotersAssociatedNew.append(info)
                        promoters = promotersAssociatedNew
                    #Get description
                    try:
                        description = getattr(genes.get_geneDescription(geneId),"description")
                    except:
                        description = ""
        else:
            error = Errors.NOT_VALID
            ##Si no es válido, busco similares
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
                similar = "tooLong"
        return render(request, self.template, {
            'geneId': geneId,
            'geneCode': geneCode,
            'promoters': promoters,
            'barPlotPromoters':barPlotPromoters,
            'enhancers': enhancers,
            'barPlotEnhancers':barPlotEnhancers,
            'tLights': tLights,
            'barPlotTLights':barPlotTLights,
            'description':description,
            'baseLink': baseLink,
            'query_form': form,
            'error': error,
            'similar':similar
        })   

class GenesAssociatedGET(TemplateView):
    template = 'queryGene.html'

    def get(self, request, gene):

        form = QueryGene()
        error = None
        promotersAssociated = []
        enhancersAssociated = []
        tLightsAssociated = []
        description = ""
        gTEX = []

        baseLink = settings.SUB_SITE+"/querySNP/snp/"
        geneId = gene
        geneCode = getGencode.getGencodeID(geneId)

        ##GET PROMOTERS
        promotersAssociated = snpsAssociated_FDR_promotersEPD.get_SNPs_Promoters(geneId)

        ##GET ENHANCERS

        enhancersAssociated = snpsAssociated_FDR_enhancers.get_Enhancers(geneId)

        ##GET TLIGHTS

        tLightsAssociated = snpsAssociated_FDR_trafficLights.get_trafficLights(geneId)

        if geneId is not '':
            #Check if gene is not associated or not in our DB
            if promotersAssociated is None and enhancersAssociated==None and tLightsAssociated==None:
                geneInDB = getGeneID.get_Genes(geneId)
                if geneInDB!=None:
                    error = Errors.NOT_ASSOCIATED
                else:
                    error = Errors.NOT_VALID
            else:
                #Get Expression
                expression = requests.get("https://gtexportal.org/rest/v1/expression/geneExpression?datasetId=gtex_v7&gencodeId="+geneCode+"&format=json").json()['geneExpression']
                gTEX = plotExpression(expression)
                # Añado a promoters el count
                if promotersAssociated:
                    promotersAssociatedNew = []
                    for gene in promotersAssociated:
                        chromStart = snpsAssociated_FDR_chrom.get_SNP_chrom(gene[1].snpID).chromStart
                        info = {
                            'data': gene[1],
                            'count': gene[0],
                            'link': settings.SUB_SITE+"/querySNP/snp/"+gene[1].snpID,
                            'distance': abs((gene[1].chromStartPromoter)-(chromStart))
                        }
                        promotersAssociatedNew.append(info)
                    promotersAssociated = promotersAssociatedNew
                #Get description
                description = getattr(genes.get_geneDescription(geneId),"description")

        else:
            error = Errors.NOT_VALID
        return render(request, self.template, {
            'geneId': geneId,
            'promotersAssociated': promotersAssociated,
            'enhancersAssociated': enhancersAssociated,
            'tLightsAssociated': tLightsAssociated,
            'description':description,
            'baseLink': baseLink,
            'gTEX':gTEX,
            'query_form': form,
            'error': error
        })   