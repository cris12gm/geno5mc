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

from .models import snpsAssociated_FDR_promotersEPD,getMethylation,getGenotype,snpsAssociated_FDR_enhancers
from sqlalchemy import inspect
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.express as px
import pandas as pd


# Create your views here.
def PlotPromoters(snpID,geneID,start,end):
    cpgs = snpsAssociated_FDR_promotersEPD.get_SNPs_Promoters(snpID,geneID)
    genotypes = getGenotype.getGenotypeCpG(snpID)

    ref = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"reference"))
    alt = str(getattr(genotypes,"alternative"))+str(getattr(genotypes,"alternative"))
    het = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"alternative"))

    valuesPlot = {}
    valuesPlot["methRatio"] = []
    valuesPlot["Genotype"] = []
    valuesPlot["CpG ID"] = []
    valuesPlot["Sample"] = []

    numSamples = 0
    for element in cpgs:
        numSamples = numSamples + 1
        idCpG = element.chrom+"_"+str(element.chromStartCpG)
        methylationCpG = getMethylation.getMethCpG(idCpG)

        ##Get names of columns
        inst = inspect(methylationCpG)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        
        for att in attr_names:
            valueMeth = getattr(methylationCpG,att)
            if valueMeth and not "_" in str(valueMeth):
                valueGenotype = str(int(getattr(genotypes,att))).replace("0",ref).replace("1",het).replace("2",alt)
                valuesPlot["methRatio"].append(valueMeth)
                valuesPlot["Genotype"].append(valueGenotype)
                valuesPlot["CpG ID"].append(idCpG)
                valuesPlot["Sample"].append(att)
        
    df = pd.DataFrame(data=valuesPlot)

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Genotype', stripmode='overlay', hover_data=["Sample"])

    fig.update_layout(
        width=300*numSamples,legend_orientation="h",legend_title='<b> Genotype </b>'
    )

    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')
    return div_obj


def PlotEnhancers(snpID,enhancerID,start,end):
    cpgs = snpsAssociated_FDR_enhancers.get_Enhancers(snpID,enhancerID)
    genotypes = getGenotype.getGenotypeCpG(snpID)
    numSamples = 0
    
    ref = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"reference"))
    alt = str(getattr(genotypes,"alternative"))+str(getattr(genotypes,"alternative"))
    het = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"alternative"))
    
    valuesPlot = {}
    valuesPlot["methRatio"] = []
    valuesPlot["Genotype"] = []
    valuesPlot["CpG ID"] = []
    valuesPlot["Sample"] = []
    
    for element in cpgs:
        numSamples = numSamples + 1
        idCpG = element.chrom+"_"+str(element.chromStartCpG)
        methylationCpG = getMethylation.getMethCpG(idCpG)

        ##Get names of columns
        inst = inspect(methylationCpG)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        
        for att in attr_names:
            valueMeth = getattr(methylationCpG,att)
            if valueMeth and not "_" in str(valueMeth):
                valueGenotype = str(int(getattr(genotypes,att))).replace("0",ref).replace("1",het).replace("2",alt)
                valuesPlot["methRatio"].append(valueMeth)
                valuesPlot["Genotype"].append(valueGenotype)
                valuesPlot["CpG ID"].append(idCpG)
                valuesPlot["Sample"].append(att)
        
    df = pd.DataFrame(data=valuesPlot)

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Genotype', stripmode='overlay', hover_data=["Sample"])
    fig.update_layout(
        width=150*numSamples,legend_orientation="h",legend_title='<b> Genotype </b>'
    )
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')
    return div_obj

class plotElements(TemplateView):
    template = "plotElement.html"

    def post(self,request):
        pass
        return render(request, self.template, {})

    def get(self,request):
        valoresGet = request.GET
        element = valoresGet['element']
        if element == 'promoter':
            plotElement = PlotPromoters(valoresGet['snp'],valoresGet['name'],valoresGet['start'],valoresGet['end'])
        elif element == 'enhancer':
            plotElement = PlotEnhancers(valoresGet['snp'],valoresGet['name'],valoresGet['start'],valoresGet['end'])
        
        return render(request, self.template, {
            'plotElement':plotElement,
            'snpID':valoresGet['snp'],
            'name':valoresGet['name']
            })