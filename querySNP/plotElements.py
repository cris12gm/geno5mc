import plotly.graph_objs as go
from plotly.offline import plot


from django.conf import settings

def plotPromoters(inputDict):
    baseLink = settings.SUB_SITE+"/plotElement/?element=promoter;snp="
    xValues = []
    yValues = []
    numSamples = 0
    for element in inputDict:
        xValue = "<a href='"+baseLink+element['data'].snpID+";name="+element['data'].geneID+";start="+str(element['data'].chromStartPromoter)+";end="+str(element['data'].chromEndPromoter)+"'target = '_self'>"+element['data'].geneID+"</a>"
        xValues.append(xValue)
        yValues.append(element['count'])
        numSamples = numSamples + 1

    layout = go.Layout(width=300*numSamples,height=580)
    fig = go.Figure(data=[
        go.Bar(name='Genes with CpG associated in its promoter', x=xValues, y=yValues, marker_color='rgb(55, 83, 109)')],layout=layout)

    div_obj = plot(fig, show_link=False, auto_open=False, include_plotlyjs=True, output_type = 'div')
    return div_obj

def plotEnhancers(inputDict):
    baseLink = settings.SUB_SITE+"/plotElement/?element=enhancer;snp="
    xValues = []
    yValues = []
    numSamples = 0
    for element in inputDict:
        yValues.append(element[0])
        xValue = "<a href='"+baseLink+element[1].snpID+";name="+element[1].enhancerID+";start="+str(element[1].chromStart)+";end="+str(element[1].chromEnd)+"'target = '_self'>"+element[1].enhancerID+"</a>"
        xValues.append(xValue)
        numSamples = numSamples + 1

    layout = go.Layout(width=150*numSamples,height=580)
    fig = go.Figure(data=[
        go.Bar(name='Enhancers with CpG associated', x=xValues, y=yValues, marker_color='rgb(55, 83, 109)')],layout=layout)
    
    div_obj = plot(fig, show_link=False, auto_open=False, include_plotlyjs=True, output_type = 'div')
    return div_obj