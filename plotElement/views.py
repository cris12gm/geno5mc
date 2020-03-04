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

from .models import snpsAssociated_FDR_promotersEPD,getMethylation,getGenotype,snpsAssociated_FDR_enhancers,snpsAssociated_FDR_trafficLights,samples,genes
from sqlalchemy import inspect
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.express as px
import pandas as pd

def PlotTLights(snpID,geneID):
    cpgs = snpsAssociated_FDR_trafficLights.get_trafficLights(snpID,geneID)
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

    samplesAll = samples.get_all_samples()
    samplesDict = {}
    for element in samplesAll:
        srx = getattr(element,"SRX")
        name = getattr(element,"internalID")
        samplesDict[name]=srx

    for element in cpgs:
        numSamples = numSamples + 1
        idCpG = element.chrom+"_"+str(element.chromStartTL)
        methylationCpG = getMethylation.getMethCpG(idCpG)

        ##Get names of columns
        inst = inspect(methylationCpG)
        attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        
        for att in attr_names:
            valueMeth = getattr(methylationCpG,att)
            if valueMeth and not "_" in str(valueMeth):
                valueGenotype = str(int(getattr(genotypes,att))).replace("0",ref).replace("1",het).replace("2",alt)
                #sample = getattr(samples.get_one_sample(att),"SRX").strip()
                valuesPlot["methRatio"].append(valueMeth)
                valuesPlot["Genotype"].append(valueGenotype)
                valuesPlot["CpG ID"].append(idCpG)
                valuesPlot["Sample"].append(samplesDict[att])
        
    df = pd.DataFrame(data=valuesPlot)

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Genotype', stripmode='group', hover_data=["Sample"], width=250*numSamples)

    fig.update_layout(
        height=550,legend_orientation="h",xaxis_tickfont_size=14, legend_title='<b>Genotype</b>'
    )
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')
    return div_obj

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

    samplesAll = samples.get_all_samples()
    samplesDict = {}
    for element in samplesAll:
        srx = getattr(element,"SRX")
        name = getattr(element,"internalID")
        samplesDict[name]=srx

    valuesPlot_Position=[]
    valuesPlot_Position_y=[1]*len(cpgs)
    hoverPosition = []

    for element in cpgs:
        numSamples = numSamples + 1
        idCpG = element.chrom+"_"+str(element.chromStartCpG)
        valuesPlot_Position.append(element.chromStartCpG)
        hoverPosition.append(idCpG)
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
                valuesPlot["Sample"].append(samplesDict[att])
        
    df = pd.DataFrame(data=valuesPlot)

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Genotype', stripmode='group', hover_data=["Sample"])

    fig.update_layout(
        width=300*numSamples, height=550,legend_orientation="h",xaxis_tickfont_size=14, legend_title='<b>Genotype</b>'
    )
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')


    fig_Distances = go.Figure(data = go.Scatter(x=valuesPlot_Position,y=valuesPlot_Position_y,mode='markers',hovertext=hoverPosition,hoverinfo="text"))

    fig_Distances.update_yaxes(showticklabels=False,title_text='', range=[0,2])
    fig_Distances.update_layout(yaxis_showgrid=False)
    fig_Distances.update_xaxes(range=[int(start)-100,int(end)+100])
    fig_Distances.add_shape(
        # Rectangle reference to the axes
            type="rect",
            xref="x",
            yref="y",
            x0=start,
            y0=0.5,
            x1=end,
            y1=1.5,
            fillcolor="PaleTurquoise",
            opacity=0.3,
        )
    div_obj2 = plot(fig_Distances,show_link=False, auto_open=False, output_type='div')

    return div_obj,div_obj2

def PlotEnhancers(snpID,enhancerID,start,end):
    cpgs = snpsAssociated_FDR_enhancers.get_Enhancers(snpID,enhancerID)
    genotypes = getGenotype.getGenotypeCpG(snpID)
    numSamples = 0

    samplesAll = samples.get_all_samples()
    samplesDict = {}
    for element in samplesAll:
        srx = getattr(element,"SRX")
        name = getattr(element,"internalID")
        samplesDict[name]=srx
    
    ref = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"reference"))
    alt = str(getattr(genotypes,"alternative"))+str(getattr(genotypes,"alternative"))
    het = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"alternative"))
    
    valuesPlot = {}
    valuesPlot["methRatio"] = []
    valuesPlot["Genotype"] = []
    valuesPlot["CpG ID"] = []
    valuesPlot["Sample"] = []
    
    valuesPlot_Position=[]
    valuesPlot_Position_y=[1]*len(cpgs)
    hoverPosition = []

    for element in cpgs:
        numSamples = numSamples + 1
        idCpG = element.chrom+"_"+str(element.chromStartCpG)
        valuesPlot_Position.append(element.chromStartCpG)
        hoverPosition.append(idCpG)
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
                valuesPlot["Sample"].append(samplesDict[att])

    df = pd.DataFrame(data=valuesPlot)

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Genotype', stripmode='group', hover_data=["Sample"])
    #stripmode='overlay' to group 
    fig.update_layout(
        width=300*numSamples, height=550, legend_orientation="h",legend_title='<b> Genotype </b>',xaxis_tickfont_size=14
    )
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')

    fig_Distances = go.Figure(data = go.Scatter(x=valuesPlot_Position,y=valuesPlot_Position_y,mode='markers',hovertext=hoverPosition,hoverinfo="text"))

    fig_Distances.update_yaxes(showticklabels=False,title_text='', range=[0,2])
    fig_Distances.update_layout(yaxis_showgrid=False)
    fig_Distances.update_xaxes(range=[int(start)-1000,int(end)+1000])
    fig_Distances.add_shape(
        # Rectangle reference to the axes
            type="rect",
            xref="x",
            yref="y",
            x0=start,
            y0=0.5,
            x1=end,
            y1=1.5,
            fillcolor="PaleTurquoise",
            opacity=0.3,
        )
    div_obj2 = plot(fig_Distances,show_link=False, auto_open=False, output_type='div')

    return div_obj, div_obj2


class plotElements(TemplateView):
    template = "plotElement.html"

    def post(self,request):
        pass
        return render(request, self.template, {})

    def get(self,request):
        valoresGet = request.GET
        element = valoresGet['element']
        description = ""
        plotElementDistance = []
        if element == 'promoter':
            plotElement,plotElementDistance = PlotPromoters(valoresGet['snp'],valoresGet['name'],valoresGet['start'],valoresGet['end'])
            description = getattr(genes.get_geneDescription(valoresGet['name']),"description")
        elif element == 'enhancer':
            plotElement,plotElementDistance = PlotEnhancers(valoresGet['snp'],valoresGet['name'],valoresGet['start'],valoresGet['end'])
        elif element== 'tLight':
            plotElement = PlotTLights(valoresGet['snp'],valoresGet['name'])
        return render(request, self.template, {
            'description':description,
            'plotElement':plotElement,
            'plotElementDistance':plotElementDistance,
            'snpID':valoresGet['snp'],
            'name':valoresGet['name']
            })

class plotElementsTour(TemplateView):
    template = "querySNP_Tour_2.html"

    def post(self,request):
        pass
        return render(request, self.template, {})

    def get(self,request):
        valoresGet = request.GET
        element = valoresGet['element']
        description = ""

        if element == 'promoter':
            plotElement = PlotPromoters(valoresGet['snp'],valoresGet['name'],valoresGet['start'],valoresGet['end'])
            description = getattr(genes.get_geneDescription(valoresGet['name']),"description")
        elif element == 'enhancer':
            plotElement = PlotEnhancers(valoresGet['snp'],valoresGet['name'],valoresGet['start'],valoresGet['end'])
        elif element== 'tLight':
            plotElement = PlotTLights(valoresGet['snp'],valoresGet['name'])
        return render(request, self.template, {
            'description':description,
            'plotElement':plotElement,
            'snpID':valoresGet['snp'],
            'name':valoresGet['name']
            })
