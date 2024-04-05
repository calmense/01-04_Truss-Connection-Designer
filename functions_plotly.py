from math import *
import plotly.graph_objects as go
import streamlit as st
from functions_member_checks import *



# Visualization with Plotly

def add_text(fig, text, xPosition, yPosition, textSize):
    fig.add_annotation(dict(font=dict(size=textSize, color = "black"),
                                            x = xPosition,
                                            y = yPosition,
                                            showarrow=False,
                                            text=text,
                                            textangle=0,
                                            xanchor='left',
                                            xref="x",
                                            yref="y"))

def plotly_go_scatter_shape(xList, yList, fillColor, lineColor, opacity):

    go_scatter = go.Scatter(
        x = xList, 
        y = yList, 
        fillcolor = fillColor, # 'rgba(0, 100, 80, 0.2)', 'lightgrey'
        line = dict(color = lineColor),
        mode = "lines", # "markers", "lines", "lines+markers", "lines+markers+text"
        fill = "toself", 
        opacity = opacity)
    return go_scatter


def plotly_go_scatter_marker(xList, yList, markerSize, markerColor):

    go_scatter = go.Scatter(
        x = xList, 
        y = yList, 
        mode = "markers", # "markers", "lines", "lines+markers", "lines+markers+text"
        marker = dict( size = markerSize,
                      color = markerColor))
    return go_scatter

def plotly_go_scatter_marker2(xList, yList, markerSize, markerColor):

    go_scatter = go.Scatter(
        x = xList, 
        y = yList, 
        mode = "markers", # "markers", "lines", "lines+markers", "lines+markers+text"
        marker = dict(size = markerSize, color = markerColor))
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
        


def rotateAroundPoint(xCoordinates, yCoordinates, angle, origin):

    xCoordinatesRotated = []
    yCoordinatesRotated = []
    angle = radians(angle)

    for i in range(len(xCoordinates)):

        x = xCoordinates[i]
        y = yCoordinates[i]
        ox, oy = origin
        qx = ox + cos(angle) * (x - ox) + sin(angle) * (y - oy)
        qy = oy + -sin(angle) * (x - ox) + cos(angle) * (y - oy)

        xCoordinatesRotated.append(round(qx))
        yCoordinatesRotated.append(round(qy))

    return xCoordinatesRotated, yCoordinatesRotated

def createLine(x1, y1, x2, y2):
    m = (y2-y1) / (x2 - x1)
    c = y2 - y1
    return c, m

def getIntersection(c1, m1, c2, m2):
    x = (c1 - c2) / (m2 - m1)
    y = m1 * x + c1
    return x, y

def draw_line(fig, xList, yList, size, color, opacity):
    fig.add_trace(go.Scatter(x = list(reversed(xList)), y = list(reversed(yList)), 
                             mode="lines", line=dict(color=color, width=size / 2), opacity=opacity))

def drawArrow(fig, xList, yList, size, color):
    fig.add_trace(go.Scatter(x = list(xList), y = list(yList), 
                             mode="lines+markers", marker=dict(color=color, size=size, symbol = "arrow", angleref = "previous")))

def generate_color_scale(data_list):
    # Find the min and max values in the list
    min_value = min(data_list)
    max_value = max(data_list)
    steps = (max_value - min_value) / 10

    # Generate color shades for each value in the list based on the min and max values
    color_scale = [
        f'rgba(255, {int(255 * (1 - (steps) / (max_value - min_value)))}, 0, 1)'
        for steps in range(10)
    ]

    return color_scale

def get_colorIndex(data_list):
    indexList = []
    minValue = min(data_list)
    maxValue = max(data_list)
    steps = (maxValue - minValue) / 9

    for value in data_list:

        # Calculate the index based on the total number of colors
        index = int((value - minValue) / steps)
        indexList.append(index)

    return indexList



def draw_arrow(fig, xList, yList, direction, scaleX, scaleY):
    lineWidth = 1
    fig.add_trace(go.Scatter(x = xList, y = yList, 
                            line=dict(width=lineWidth),
                            marker= dict(size=8,symbol= "arrow", angleref="previous", color='black')))
       
    fig.add_trace(go.Scatter(x = list(reversed(xList)), y = list(reversed(yList)),
                             line=dict(width=lineWidth),
                            marker= dict(size=8,symbol= "arrow", angleref="previous", color='black')))
    
    if direction == "X":
        xLine1 = [xList[0], xList[0]]
        yLine1 = [yList[0] - 5*scaleY, yList[0] + 5*scaleY]

        xLine2 = [xList[-1], xList[-1]]
        yLine2 = [yList[-1] - 5*scaleY, yList[-1] + 5*scaleY]

    elif direction == "Y":
        xLine1 = [xList[0] - 5*scaleY, xList[0] + 5*scaleY]
        yLine1 = [yList[0], yList[0]]

        xLine2 = [xList[-1] - 5*scaleY, xList[-1] + 5*scaleY]
        yLine2 = [yList[-1], yList[-1]]

    fig.add_trace(go.Scatter(x=xLine1, y = yLine1, mode="lines", marker=dict(color='black'), line=dict(width=lineWidth)))
    fig.add_trace(go.Scatter(x=xLine2, y = yLine2, mode="lines", marker=dict(color='black', angle = 45), line=dict(width=lineWidth)))



def drawDistances(beam):

    a = 50

    a1 = beam.distancesFinal[0][0]
    a2 = beam.distancesFinal[0][1]
    a3 = beam.distancesFinal[0][2]
    a4 = beam.distancesFinal[0][3]
    e1 = beam.distancesFinal[0][4]
               
    xCords = [0, 2*a + beam.sheetLength, 2*a + beam.sheetLength, 0, 0]
    yCords = [0, 0, 2*a + beam.height, 2*a + beam.height, 0]
    
    #fig = go.Figure(plotly_go_scatter_shape(xCords, yCords, "white", "black", 0.5))

    # fastener
    xList = [a, a + beam.sheetLength, a + beam.sheetLength, a, a]
    yList = [a, a, a + beam.height, a + beam.height, a]

    fig = go.Figure(plotly_go_scatter_shape(xList, yList, "rgba(0, 100, 80, 0.2)", "rgba(244, 232, 205, 100)", 0.8))
    #fig.add_trace(go_scatter)

    for i in range(len(beam.xCoordinates[0])):

            x = beam.xCoordinates[0][i] +a
            y = beam.yCoordinates[0][i] +a

            # bolt markers
            go_scatter = plotly_go_scatter_marker([x], [y], beam.fastenerDiameter, "black")
            fig.add_trace(go_scatter)

    # dimension in X
    a_3 = draw_arrow(fig, [a, a + a3], [a/2, a/2], "X", 1, 1)
    a_1 = draw_arrow(fig, [a + a3, a + a3 + a1], [a/2, a/2], "X", 1, 1)
    e_1 = draw_arrow(fig, [a + a3 + a1, a + a3 + a1 + e1], [a/2, a/2], "X", 1, 1)

    # dimension in Y
    a_4 = draw_arrow(fig, [a/2, a/2], [a, a + a4], "Y", 1, 1)
    a_2 = draw_arrow(fig, [a/2, a/2], [a + a4, a + a4 + a2], "Y", 1, 1)

    # add text X
    textsize = 14
    add_text(fig, "a3", a + a3/4, a/3, textsize)
    add_text(fig, "a1", a + a3 + a1/4, a/3, textsize)
    add_text(fig, "e1", a + a3 + a1 + e1/4, a/3, textsize)

    add_text(fig, "a4", a/5, a + a4/2, textsize)
    add_text(fig, "a2", a/5, a + a4 + a2/2, textsize)


    # Set the aspect ratio to be equal
    fig.update_layout(
        xaxis=dict(scaleanchor="y", scaleratio=1,fixedrange=True, visible=False),
        yaxis=dict(scaleanchor="x", scaleratio=1, fixedrange=True, visible=False),
        uirevision='static',
        width = 500,
        height = 500,
        showlegend=False)  # Disable zoom functionality

    # Hide the axis
    fig.update_xaxes(showline=False, showgrid=False, zeroline=False, rangemode="tozero")
    fig.update_yaxes(showline=False, showgrid=False, zeroline=False, rangemode="tozero")

    fig.update_xaxes(range=[200, a + beam.sheetLength])
    fig.update_yaxes(range=[0, a + beam.height])

    st.write(fig)
    

def drawSheets(ClassList):

    # colors
    fillColor = 'rgba(62, 140, 163, 1)'
    lineColor = 'rgba(244, 232, 205, 0)'

    # base sheet
    beam = ClassList[0]
    xList = [-beam.height / 2, beam.height / 2, beam.height / 2, -beam.height / 2, -beam.height / 2]
    yList = [0, 0, ClassList[0].height, ClassList[0].height, 0]

    fig = go.Figure(plotly_go_scatter_shape(xList, yList, fillColor, lineColor, 1))

    # sheets
    for i in range(len(ClassList)):

        beam = ClassList[i]
        gapX = ClassList[0].height / 2 * sin(radians(beam.beamAngle)) 
        gapY = ClassList[0].height / 2 - beam.height / 2

        sheetLengthFactor = 1
        origin = (0, ClassList[0].height / 2)

        xList = [gapX, gapX + beam.sheetLength * sheetLengthFactor, gapX + beam.sheetLength * sheetLengthFactor, gapX, gapX]
        yList = [gapY, gapY, beam.height + gapY, beam.height + gapY, gapY]

        xCords, yCords = rotateAroundPoint(xList, yList, -beam.beamAngle, origin)
        fig.add_trace(plotly_go_scatter_shape(xCords, yCords, fillColor, lineColor, 1))

    # fasteners
    for i in range(len(ClassList)):

        beam = ClassList[i]

        for i in range(len(beam.xCoordinates[0])):

            x = beam.xCoordinates[0][i] 
            y = beam.yCoordinates[0][i] 

            # bolt markers
            go_scatter = plotly_go_scatter_marker([x], [y], beam.fastenerDiameter, "black")
            fig.add_trace(go_scatter)

    # write utilization
    text = r'''Sheet ''' + str(ClassList[0].sheetGrade) + r''' no =  ''' + str(ClassList[0].sheetNo)
    add_text(fig, text, 800, 650, 20)

    text = r'''Fastener ''' + str(ClassList[0].fastenerGrade) + r''' ⌀ = ''' + str(ClassList[0].fastenerDiameter)
    add_text(fig, text, 800, 600, 20)

    # write utilization    
    text = r'''max Utilization'''
    add_text(fig, text, 800, 450, 20)
    fastenerCheckMax, tensionMemberCheckMax, compressionMemberMax, axialBlockFailureMax, fastenerCheckMaxIndex, tensionMemberCheckMaxIndex, compressionMemberMaxIndex, axialBlockFailureMaxIndex = getEtaMax(ClassList)
    
    textStress = r'''Stress η = ''' + str(int(max(tensionMemberCheckMax, compressionMemberMax) * 100)) + r'''% Beam ''' + str(tensionMemberCheckMaxIndex + 1)
    add_text(fig, textStress, 800, 400, 20)

    textJoint = r'''Joint η = ''' + str(int(fastenerCheckMax * 100)) + r'''% Beam ''' + str(fastenerCheckMaxIndex + 1)
    add_text(fig, textJoint, 800, 350, 20)

    textSheet = r'''Sheet η = ''' + str(int(axialBlockFailureMax * 100)) + r'''% Beam ''' + str(axialBlockFailureMaxIndex + 1)
    add_text(fig, textSheet, 800, 300, 20)

    fig.update_layout(
        xaxis=dict(scaleanchor="y", scaleratio=1,fixedrange=False, visible=False),
        yaxis=dict(scaleanchor="x", scaleratio=1, fixedrange=False, visible=False),
        uirevision='static',
        width = 1000,
        height = 600,
        showlegend=False)  # Disable zoom functionality
    
    st.write(fig)
