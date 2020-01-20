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

from .forms import QueryGene
from .models import snpsAssociated_FDR_promotersEPD, snpsAssociated_FDR_chrom, getGeneID

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
        promotersAssociated = []

        if form.is_valid():
            geneId = form.cleaned_data.get('GeneId')
            promotersAssociated = snpsAssociated_FDR_promotersEPD.get_SNPs_Promoters(geneId)
            if geneId is not '':
                if promotersAssociated is None:
                    geneInDB = getGeneID.get_Genes(geneId)
                    if geneInDB!=None:
                        error = Errors.NOT_ASSOCIATED
                    else:
                        error = Errors.NOT_VALID
                else:
                    # Añado a genes el count
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
            'query_form': form,
            'error': error
        })   

class GenesAssociatedGET(TemplateView):
    template = 'queryGeneWF.html'

    def get(self, request, gene):

        form = QueryGene()
        error = None
        promotersAssociated = []

        geneId = gene
        promotersAssociated = snpsAssociated_FDR_promotersEPD.get_SNPs_Promoters(geneId)
        if geneId is not '':
            if promotersAssociated is None:
                geneInDB = getGeneID.get_Genes(geneId)
                if geneInDB!=None:
                    error = Errors.NOT_ASSOCIATED
                else:
                    error = Errors.NOT_VALID
            else:
                # Añado a genes el count
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
            'query_form': form,
            'error': error
        })   