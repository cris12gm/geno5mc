import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
import plotly.express as px
from sqlalchemy import inspect

from django.conf import settings

from .models import getMethylation,getGenotype,snpsAssociated_FDR_promotersEPD,snpsAssociated_FDR_trafficLights

def plotTrafficLights(snpID,geneID):

    div_obj = ""
    inputList = snpsAssociated_FDR_trafficLights.get_trafficLights_SNP(geneID,snpID)

    cpgs = {}
    for element in inputList:
        cpg = element.chrom+"_"+str(element.chromStartTL)
        cpgs[cpg] = ""
   
    # Get meth     

    valuesPlot = {}
    valuesPlot["methRatio"] = []
    valuesPlot["CpG ID"] = []
    valuesPlot["Sample"] = []
    valuesPlot["Genotype"] = []

    genotypes = getGenotype.getGenotypeCpG(snpID)
    ref = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"reference"))
    alt = str(getattr(genotypes,"alternative"))+str(getattr(genotypes,"alternative"))
    het = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"alternative"))

    for cpg in cpgs:
        methylationCpG = getMethylation.getMethCpG(cpg)
        if methylationCpG:
            inst = inspect(methylationCpG)
            attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
            for att in attr_names:
                valueMeth = getattr(methylationCpG,att)             
                if valueMeth and not "_" in str(valueMeth):
                    valueGenotype = str(int(getattr(genotypes,att))).replace("0",ref).replace("1",het).replace("2",alt)
                    valuesPlot["methRatio"].append(valueMeth)
                    valuesPlot["Sample"].append(att)  
                    valuesPlot["Genotype"].append(valueGenotype)
                    valuesPlot["CpG ID"].append(cpg)
    df = pd.DataFrame(data=valuesPlot)

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Genotype', hover_data=["Sample"],category_orders={"Genotype":[ref,het,alt]})

    fig.update_layout(width=200*len(cpgs), height=500,legend_orientation="h",xaxis_tickfont_size=14)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')

    return div_obj

def plotPromoter(inputID,snpID):
    
    div_obj = ""
    inputList = snpsAssociated_FDR_promotersEPD.get_Promoter_SNP_Id(inputID,snpID)

    for element in inputList:
        try:
            cpgs = outputList[2]
        except:
            cpgs = {}
    
        cpg = element.chrom+"_"+str(element.chromStartCpG)
        cpgs[cpg]=""
        chrom = element.chrom
        coordinates = "<b>"+inputID+"</b> "+element.chrom+":"+str(element.chromStartPromoter)+"-"+str(element.chromEndPromoter)
        outputList = [element.chromStartPromoter,element.chromEndPromoter,cpgs,chrom]

    #Get meth

    valuesPlot = {}
    valuesPlot["methRatio"] = []
    valuesPlot["CpG ID"] = []
    valuesPlot["Sample"] = []
    valuesPlot["Genotype"] = []

    cpgs = outputList[2]    
    start = int(outputList[0])
    end = int(outputList[1])
    chrom = outputList[3]

    genotypes = getGenotype.getGenotypeCpG(snpID)
    ref = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"reference"))
    alt = str(getattr(genotypes,"alternative"))+str(getattr(genotypes,"alternative"))
    het = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"alternative"))

    #Gene in minus strand
    if start>end:
        start = end
        end = int(outputList[1]) 

    numCpGs = 0
    for i in range(start,end):
        idElement = chrom+"_"+str(i)
        methylationCpG = getMethylation.getMethCpG(idElement)
        if methylationCpG:
            numCpGs = numCpGs + 1
            inst = inspect(methylationCpG)
            attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
            for att in attr_names:
                valueMeth = getattr(methylationCpG,att)           
                if valueMeth and not "_" in str(valueMeth):
                    valueGenotype = str(int(getattr(genotypes,att))).replace("0",ref).replace("1",het).replace("2",alt)
                    valuesPlot["methRatio"].append(valueMeth)
                    valuesPlot["Sample"].append(att)  
                    valuesPlot["Genotype"].append(valueGenotype)
                    try:
                        cpgs[idElement]
                        valuesPlot["CpG ID"].append("<b style='color:red';>"+idElement+"</b>")
                    except:
                        valuesPlot["CpG ID"].append(idElement)
    
    df = pd.DataFrame(data=valuesPlot)

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Genotype', hover_data=["Sample"],category_orders={"Genotype":[ref,het,alt]})

    fig.update_layout(width=200*numCpGs, height=500,legend_orientation="h",xaxis_tickfont_size=14)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')

    return div_obj,coordinates