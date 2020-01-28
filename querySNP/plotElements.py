import plotly.graph_objs as go
from plotly.offline import plot

from django.conf import settings

def plotPromoters(inputDict):
    baseLink = settings.SUB_SITE+"/plotElement/?element=promoter;snp="
    xValues = []
    yValues = []
    for element in inputDict:
        xValue = "<a href='"+baseLink+element['data'].snpID+";name="+element['data'].geneID+";start="+str(element['data'].chromStartPromoter)+";end="+str(element['data'].chromEndPromoter)+"'>"+element['data'].geneID+"</a>"
        xValues.append(xValue)
        yValues.append(element['count'])

    layout = go.Layout(autosize=True,height=580)
    fig = go.Figure(data=[
        go.Bar(name='Genes with CpG associated in its promoter', x=xValues, y=yValues)],layout=layout)

    div_obj = plot(fig, show_link=False, auto_open=False, include_plotlyjs=True, output_type = 'div')
    return div_obj