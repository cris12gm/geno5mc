import plotly.graph_objs as go
from plotly.offline import plot

def plotElement(inputDict):
    xValues = []
    yValues = []
    for element in inputDict:
        xValues.append(element['data'].geneID)
        yValues.append(element['count'])

    fig = go.Figure(data=[
        go.Bar(name='Genes with CpG associated in its promoter', x=xValues, y=yValues)])

    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')
    return div_obj