import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
import plotly.express as px
from sqlalchemy import inspect

from django.conf import settings

from .models import getMethylation,getGenotype


def plotRegion(inputID,associated):
    
    div_obj = ""

    inputID = inputID.split("-")
    chrom = inputID[0]
    start = int(inputID[1])
    end = int(inputID[2])
    cpgs = {}

    for key in associated:
        cpgs[int(key)]=True

    # #Get meth

    valuesPlot = {}
    valuesPlot["methRatio"] = []
    valuesPlot["CpG ID"] = []
    valuesPlot["Sample"] = []
    valuesPlot["Associated"] = []

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
                        cpgs[i]
                        valuesPlot["Associated"].append("YES")
                    except:
                        valuesPlot["Associated"].append("NO")
    
    df = pd.DataFrame(data=valuesPlot)

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Associated', hover_data=["Sample"] )

    fig.update_layout(width=1000, height=500,legend_orientation="h",xaxis_tickfont_size=14)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')

    return div_obj

def plotRegionBySNP(inputID,associated,snpID):
    
    div_obj = ""

    inputID = inputID.split("-")
    chrom = inputID[0]
    start = int(inputID[1])
    end = int(inputID[2])
    cpgs = {}

    for key in associated:
        cpgs[int(key)]=True

    # Get genotypes

    genotypes = getGenotype.getGenotypeCpG(snpID)
    ref = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"reference"))
    alt = str(getattr(genotypes,"alternative"))+str(getattr(genotypes,"alternative"))
    het = str(getattr(genotypes,"reference"))+str(getattr(genotypes,"alternative"))

    # Get meth

    valuesPlot = {}
    valuesPlot["methRatio"] = []
    valuesPlot["CpG ID"] = []
    valuesPlot["Sample"] = []
    valuesPlot["Genotype"] = []

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
                        cpgs[i]
                        valuesPlot["CpG ID"].append("<b style='color:red';>"+idElement+"</b>")
                    except:
                        valuesPlot["CpG ID"].append(idElement)
    
    df = pd.DataFrame(data=valuesPlot)

    fig = px.strip(df, 'CpG ID', 'methRatio', 'Genotype', hover_data=["Sample"],category_orders={"Genotype":[ref,het,alt]} )

    fig.update_layout(width=200*numCpGs, height=500,legend_orientation="h",xaxis_tickfont_size=14)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')

    return div_obj