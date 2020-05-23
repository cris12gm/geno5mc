import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
import plotly.express as px
from sqlalchemy import inspect

from django.conf import settings

from .models import getMethylation,snpsAssociated_FDR_promotersEPD

def plotEnhancers(inputDict):
    baseLink = settings.SUB_SITE+"/querySNP/snp/"
    xValues = []
    yValues = []
    numSamples = 0
    for element in inputDict:
        yValues.append(element.numOverlaps)
        xValue = "<a href='"+baseLink+element.snpID+"'>"+element.snpID+"</a>"
        xValues.append(xValue)
        numSamples = numSamples + 1

    ancho = 100+(numSamples*50)
    
    layout = go.Layout(width=ancho,height=400,bargap=0.1)
    fig = go.Figure(data=[
        go.Bar(name='Associated CpGs in Enhancers', x=xValues, y=yValues, marker_color='rgb(25, 74, 144)')],layout=layout)
    fig.update_layout(xaxis_tickangle=-45 ,xaxis_tickfont_size=12)
    fig.update_yaxes(title_text='<b>Count CpGs</b>')

    div_obj = plot(fig, show_link=False, auto_open=False, include_plotlyjs=True, output_type = 'div')
    return div_obj

def plotTrafficLights(inputDict):

    baseLink = settings.SUB_SITE+"/querySNP/snp/"
    xValues = []
    yValues = []
    numSamples = 0
    
    for element in inputDict:
        yValues.append(element.numOverlaps)
        xValue = "<a href='"+baseLink+element.snpID+"'>"+element.snpID+"</a>"
        xValues.append(xValue)
        numSamples = numSamples + 1

    ancho = 100+(numSamples*50)

    layout = go.Layout(width=ancho,height=400,bargap=0.1)
    fig = go.Figure(data=[
        go.Bar(name='Genes with Associated CpGs that are Traffic Lights', x=xValues, y=yValues, marker_color='rgb(25, 74, 144)')],layout=layout)
    fig.update_layout(barmode='group', xaxis_tickangle=-45, xaxis_tickfont_size=12)
    fig.update_yaxes(title_text='<b>Count CpGs</b>')

    div_obj = plot(fig, show_link=False, auto_open=False, include_plotlyjs=True, output_type = 'div')
    return div_obj

def plotPromoter(inputID):
    
    div_obj = ""

    inputList = snpsAssociated_FDR_promotersEPD.get_PromoterId(inputID)

    for element in inputList:
        try:
            cpgs = outputList[2]
        except:
            cpgs = {}
    
        cpg = element.chrom+"_"+str(element.chromStartCpG)
        cpgs[cpg]=""
        chrom = element.chrom
        outputList = [element.chromStartPromoter,element.chromEndPromoter,cpgs,chrom]

    #Get meth

    valuesPlot = {}
    valuesPlot["methRatio"] = []
    valuesPlot["CpG ID"] = []
    valuesPlot["Sample"] = []
    valuesPlot["Associated"] = []

    cpgs = outputList[2]    
    start = int(outputList[0])
    end = int(outputList[1])
    chrom = outputList[3]

    #Gene in minus strand
    if start>end:
        start = end
        end = int(outputList[1]) 

    for i in range(start,end):
        idElement = chrom+"_"+str(i)
        methylationCpG = getMethylation.getMethCpG(idElement)
        if methylationCpG:
            inst = inspect(methylationCpG)
            attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
            for att in attr_names:
                valueMeth = getattr(methylationCpG,att)
                
                if valueMeth and not "_" in str(valueMeth):
                    valuesPlot["methRatio"].append(valueMeth)
                    valuesPlot["CpG ID"].append(idElement)
                    valuesPlot["Sample"].append(att)  
                    try:
                        cpgs[idElement]
                        valuesPlot["Associated"].append("YES")
                    except:
                        valuesPlot["Associated"].append("NO")
    
    df = pd.DataFrame(data=valuesPlot)

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Associated', hover_data=["Sample"])

    fig.update_layout(width=1000, height=500,legend_orientation="h",xaxis_tickfont_size=14)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')

    return div_obj