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


from .forms import QueryGene
from .models import snpsAssociated_FDR_promotersEPD, snpsAssociated_FDR_chrom, getGeneID, snpsAssociated_FDR_enhancers, snpsAssociated_FDR_trafficLights, getGencode

class Errors(Enum):
    NO_ERROR = 0
    NOT_VALID = 1
    NOT_ASSOCIATED = 2

class GenesAssociated(TemplateView):
    template = 'queryGene.html'

    def get(self, request):  
        form = QueryGene()
        return render(request, self.template, {
            'query_form': form
        })

    def post(self, request):
        form = QueryGene(request.POST)
        error = None
        baseLink = settings.SUB_SITE+"/querySNP/snp/"

        promotersAssociated = []
        enhancersAssociated = []
        tLightsAssociated = []
        gTEX = []

        if form.is_valid():
            geneId = form.cleaned_data.get('GeneId')
            geneCode = getGencode.getGencodeID(geneId)
            
            #GET PROMOTERS
            promotersAssociated = snpsAssociated_FDR_promotersEPD.get_SNPs_Promoters(geneId)

            ##GET ENHANCERS
            enhancersAssociated = snpsAssociated_FDR_enhancers.get_Enhancers(geneId)

            ##GET TLIGHTS
            tLightsAssociated = snpsAssociated_FDR_trafficLights.get_trafficLights(geneId)
            
            if geneId is not '':
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
                    # Añado a genes el count
                    if promotersAssociated is not None:
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
        else:
            error = Errors.NOT_VALID

        return render(request, self.template, {
            'geneId': geneId,
            'promotersAssociated': promotersAssociated,
            'enhancersAssociated': enhancersAssociated,
            'tLightsAssociated': tLightsAssociated,
            'gTEX':gTEX,
            'baseLink': baseLink,
            'query_form': form,
            'error': error
        })   

class GenesAssociatedGET(TemplateView):
    template = 'queryGeneWF.html'

    def get(self, request, gene):

        form = QueryGene()
        error = None
        promotersAssociated = []
        enhancersAssociated = []
        tLightsAssociated = []
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

        else:
            error = Errors.NOT_VALID
        return render(request, self.template, {
            'geneId': geneId,
            'promotersAssociated': promotersAssociated,
            'enhancersAssociated': enhancersAssociated,
            'tLightsAssociated': tLightsAssociated,
            'baseLink': baseLink,
            'gTEX':gTEX,
            'query_form': form,
            'error': error
        })   