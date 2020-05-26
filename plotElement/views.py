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
from datetime import datetime
import requests

def downloadMethData(input,typeElement,name,snp):

    outfile = settings.MEDIA_ROOT+str(datetime.now()).split(".")[0].replace(" ","_").replace(":","_")+"_"+typeElement+"_"+name+"_"+snp+".txt"
    linkDownload = outfile.replace(settings.MEDIA_ROOT,settings.MEDIA_URL)

    output = {}
    CpGs = input['CpG ID']
    methRatio = input['methRatio']
    samples = input['Sample']
    genotype = input['Genotype']

    i = 0
    header = "Sample\tGenotype"
    cpgsAvailable = {}
    for i in range(len(samples)):
        try:
            values = output[samples[i],genotype[i]]
        except:
            values = {}
        values[CpGs[i]] = methRatio[i]
        cpgsAvailable[CpGs[i]] = ""

        output[samples[i],genotype[i]] = values
        i = i + 1

    fileToWrite = open(outfile,'w')

    for cpg in cpgsAvailable:
        header = header+"\t"+cpg
    
    fileToWrite.write(header+"\n")
    
    for sample,genotype in output:
        linea = sample+"\t"+genotype
        values = output[sample,genotype]
        for cpg in cpgsAvailable:
            try:
                methRatio = values[cpg]
            except:
                methRatio = "NA"
            linea = linea+"\t"+str(methRatio)
        linea = linea+"\n"
        fileToWrite.write(linea)

    return linkDownload

def PlotTLights(snpID,geneID):
    cpgs = snpsAssociated_FDR_trafficLights.get_trafficLights(snpID,geneID)
    genotypes = getGenotype.getGenotypeCpG(snpID)

    #Get gene position

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

    #For position Plot
    valuesPlot_Position=[]
    hoverPosition = []

    for element in cpgs:
        numSamples = numSamples + 1
        idCpG = element.chrom+"_"+str(element.chromStartTL)
        valuesPlot_Position.append(element.chromStartTL)
        hoverPosition.append(idCpG)
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

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Genotype', stripmode='group', hover_data=["Sample"] ,category_orders={"Genotype":[ref,het,alt]}, width=250*numSamples)

    fig.update_layout(
        height=500,legend_orientation="h",xaxis_tickfont_size=14, legend_title='<b>Genotype</b>'
    )
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')

    return div_obj,valuesPlot

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

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Genotype', stripmode='group', hover_data=["Sample"], category_orders={"Genotype":[ref,het,alt]})

    fig.update_layout(
        width=300*numSamples, height=500,legend_orientation="h",xaxis_tickfont_size=14, legend_title='<b>Genotype</b>'
    )
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')

    return div_obj, valuesPlot

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

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Genotype', stripmode='group', hover_data=["Sample"],category_orders={"Genotype":[ref,het,alt]})
    #stripmode='overlay' to group 
    fig.update_layout(
        width=300*numSamples, height=500, legend_orientation="h",legend_title='<b> Genotype </b>',xaxis_tickfont_size=14
    )
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')

    return div_obj,valuesPlot

class plotElements(TemplateView):
    template = "plotElement.html"

    def post(self,request):
        pass
        return render(request, self.template, {})

    def get(self,request):
         templateError = "error.html"

         try:
            valoresGet = request.GET
            element = valoresGet['element']
            description = ""
            linkDownload = ""

            if element == 'promoter':
                plotElement,valuesPlot = PlotPromoters(valoresGet['snp'],valoresGet['name'],valoresGet['start'],valoresGet['end'])
                description = getattr(genes.get_geneDescription(valoresGet['name']),"description").capitalize()
                linkDownload = downloadMethData(valuesPlot,"promoter",valoresGet['name'],valoresGet['snp'])
            elif element == 'enhancer':
                plotElement,valuesPlot = PlotEnhancers(valoresGet['snp'],valoresGet['name'],valoresGet['start'],valoresGet['end'])
                linkDownload = downloadMethData(valuesPlot,"enhancer",valoresGet['name'],valoresGet['snp'])
            elif element== 'tLight':
                plotElement,valuesPlot = PlotTLights(valoresGet['snp'],valoresGet['name'])
                linkDownload = downloadMethData(valuesPlot,"tLight",valoresGet['name'],valoresGet['snp'])
            return render(request, self.template, {
                'description':description,
                'element':element,
                'plotElement':plotElement,
                'snpID':valoresGet['snp'],
                'linkDownload':linkDownload,
                'name':valoresGet['name']
                })
         except:
             return render(request, templateError)
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
            description = getattr(genes.get_geneDescription(valoresGet['name']),"description").capitalize()
        elif element == 'enhancer':
            plotElement = PlotEnhancers(valoresGet['snp'],valoresGet['name'],valoresGet['start'],valoresGet['end'])
        elif element== 'tLight':
            plotElement = PlotTLights(valoresGet['snp'],valoresGet['name'])
        return render(request, self.template, {
            'description':description,
            'plotElement':plotElement,
            'plotElementDistance':plotElementDistance,
            'snpID':valoresGet['snp'],
            'name':valoresGet['name']
            })
