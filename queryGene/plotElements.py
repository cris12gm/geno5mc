import plotly.graph_objs as go
from plotly.offline import plot


from django.conf import settings

def plotPromoters(inputDict):
    baseLink = settings.SUB_SITE+"/querySNP/snp/"
    xValues = []
    yValues = []
    numSamples = 0
    for element in inputDict:
        xValue = "<a href='"+baseLink+element[1].snpID+"'>"+element[1].snpID+"</a>"
        xValues.append(xValue)
        yValues.append(element[0])
        numSamples = numSamples + 1
    ancho = 100+(numSamples*50)
    layout = go.Layout(width=ancho, height=400,bargap=0.1)
    fig = go.Figure(data=[
        go.Bar(name='Genes with CpG associated in its promoter', x=xValues, y=yValues, marker_color='rgb(55, 83, 109)')],layout=layout)

    fig.update_layout(xaxis_tickangle=-45,xaxis_tickfont_size=12)
    fig.update_yaxes(title_text='<b>Count CpGs</b>')
    div_obj = plot(fig, show_link=False, auto_open=False, include_plotlyjs=True, output_type = 'div')
    return div_obj

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
        go.Bar(name='Enhancers with CpG associated', x=xValues, y=yValues, marker_color='rgb(55, 83, 109)')],layout=layout)
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
        go.Bar(name='Genes with CpG associated that are Traffic Lights', x=xValues, y=yValues, marker_color='rgb(55, 83, 109)')],layout=layout)
    fig.update_layout(barmode='group', xaxis_tickangle=-45, xaxis_tickfont_size=12)
    fig.update_yaxes(title_text='<b>Count CpGs</b>')

    div_obj = plot(fig, show_link=False, auto_open=False, include_plotlyjs=True, output_type = 'div')
    return div_obj