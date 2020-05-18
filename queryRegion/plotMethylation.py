import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
import plotly.express as px
from sqlalchemy import inspect

from django.conf import settings

from .models import getMethylation


def plotRegion(inputID):
    
    div_obj = ""

    inputID = inputID.split("-")
    chromStart = inputID[1]
    chromEnd = inputID[2]

    # for element in inputList:
    #     try:
    #         cpgs = outputList[2]
    #     except:
    #         cpgs = {}
    
    #     cpg = element.chrom+"_"+str(element.chromStartCpG)
    #     cpgs[cpg]=""
    #     chrom = element.chrom
    #     outputList = [element.chromStartPromoter,element.chromEndPromoter,cpgs,chrom]

    # #Get meth

    # valuesPlot = {}
    # valuesPlot["methRatio"] = []
    # valuesPlot["CpG ID"] = []
    # valuesPlot["Sample"] = []
    # valuesPlot["Associated"] = []

    # cpgs = outputList[2]    
    # start = int(outputList[0])
    # end = int(outputList[1])
    # chrom = outputList[3]

    # #Gene in minus strand
    # if start>end:
    #     start = end
    #     end = int(outputList[1]) 

    # for i in range(start,end):
    #     idElement = chrom+"_"+str(i)
    #     methylationCpG = getMethylation.getMethCpG(idElement)
    #     if methylationCpG:
    #         inst = inspect(methylationCpG)
    #         attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    #         for att in attr_names:
    #             valueMeth = getattr(methylationCpG,att)
                
    #             if valueMeth and not "_" in str(valueMeth):
    #                 valuesPlot["methRatio"].append(valueMeth)
    #                 valuesPlot["CpG ID"].append(idElement)
    #                 valuesPlot["Sample"].append(att)  
    #                 try:
    #                     cpgs[idElement]
    #                     valuesPlot["Associated"].append("YES")
    #                 except:
    #                     valuesPlot["Associated"].append("NO")
    
    # df = pd.DataFrame(data=valuesPlot)

    # fig = px.strip(df, 'CpG ID', 'methRatio', 'Associated', hover_data=["Sample"])

    # fig.update_layout(width=1000, height=500,legend_orientation="h",xaxis_tickfont_size=14)
    # fig.update_xaxes(title_text='')
    # fig.update_yaxes(title_text='<b>Meth Ratio</b>')
    # div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')

    return div_obj