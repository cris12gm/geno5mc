import plotly.graph_objs as go
from plotly.offline import plot

def plotExpression(inputDic):

    valuesPlot = []    
    for element in inputDic:
        datosSample = go.Box(y=element['data'] ,boxpoints='outliers',
                name =  element['tissueSiteDetailId'],
                showlegend=False)
        valuesPlot.append(datosSample)

    div_obj = plot(valuesPlot, show_link=False, auto_open=False, output_type = 'div')

    return div_obj