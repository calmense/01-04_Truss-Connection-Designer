from math import pi
import plotly.graph_objects as go


# Visualization iwth Plotly

def plotly_go_scatter_shape(xList, yList, fillColor, lineColor):

    go_scatter = go.Scatter(
        x = xList, 
        y = yList, 
        fillcolor = fillColor, # 'rgba(0, 100, 80, 0.2)', 'lightgrey'
        line = dict(color = lineColor),
        mode = "lines", # "markers", "lines", "lines+markers", "lines+markers+text"
        fill = "toself" )
    return go_scatter

def plotly_go_scatter_marker(xList, yList, markerSize, markerColor):

    go_scatter = go.Scatter(
        x = xList, 
        y = yList, 
        mode = "markers", # "markers", "lines", "lines+markers", "lines+markers+text"
        marker = dict( size = markerSize,
                      color = markerColor))
    return go_scatter

def plotly_go_scatter_text(xList, yList, text, textFont, textSize, textColor, textPosition):

    go_scatter = go.Scatter(
        x = xList, 
        y = yList, 
        mode = "text", # "markers", "lines", "lines+markers", "lines+markers+text"
        text = text,
        textfont = dict( family = textFont,
                        size = textSize,
                        color = textColor)  ,
        textposition = textPosition, # 'top left', 'top center', 'top right', 'middle left', 'middle center', 'middle right', 'bottom left', 'bottom center', 'bottom right  
        )
    return go_scatter

def plotly_add_arrow(fig, xPosition, yPosition, ax, ay, arrowhead, arrowsize, arrowcolor):
        
        arrow = fig.add_annotation(
            x = xPosition,  # X-coordinate of the arrow tail
            y = yPosition,  # Y-coordinate of the arrow tail
            ax = ax,  # X-coordinate of the arrowhead
            ay = ay,  # Y-coordinate of the arrowhead
            arrowhead = arrowhead,  # Arrowhead style (2 is an arrow)
            arrowsize = arrowsize,  # Arrowhead size
            arrowcolor = arrowcolor)
