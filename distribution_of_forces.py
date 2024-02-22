# Schraubenbemessungsprogramm: Webapp mit Streamlit - Axial- und Schertragfähigkeit von Würth Vollgewindeschrauben
# Bibliotheken
from math import pi, sqrt, cos, sin, atan
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from itertools import product
from collections import defaultdict
from distribution_of_forces_functions import *



# HTML Einstellungen
st.set_page_config(page_title="Bolt Group Forces", layout="wide")
st.markdown("""<style>
[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 500px;}
[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 500px;margin-left: -500px;}
footer:after{
    content:"Cal Mense M.Eng.";
    display:block;
    position:relative;
    color:grey;
}
</style>""",unsafe_allow_html=True)

st.markdown('''
<style>
.katex-html {
    text-align: left;
}
</style>''',
unsafe_allow_html=True
)

# header
header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 40px; font-weight: bold; ">In-Plane Eccentric Shear Load</p>'
st.markdown(header, unsafe_allow_html=True)

text1 = "This program calculates the force distribution resulting from an eccentric shear load applied within the plane of the pattern."
text2 = "It assumes that the applied loads act around the centroid of the bolt pattern, employing a conservative approach. This simplifies the analysis and allows for the generalization of the analysis to any bolt pattern with various applied loading conditions."
st.write(text1, text2)

with st.sidebar:

    # Input parameter
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">Input Parameters</p>'
    st.markdown(header, unsafe_allow_html=True)

    # Geometry
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 17px; font-weight: bold; ">Geometry</p>'
    st.markdown(header, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:  
        timberWidth = int(st.text_input("Width (mm)", 200))
    with col2:  
        timberHeight = int(st.text_input("Height (mm)", 400))

    # Fastener
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 17px; font-weight: bold; ">Fastener</p>'
    st.markdown(header, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:  
        diameter = st.selectbox("Diameter (mm)", [6,8,10])
    with col2: 
        strength = st.selectbox("Strength (N/mm2)", [4.6,5.6,8.8])
        
    # Number of bolts
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 17px; font-weight: bold; ">Number of bolts</p>'
    st.markdown(header, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:  
        noVertical = int(st.slider("Vertical number", 3,8))
    with col2:
        noHorizontal = int(st.slider("Horizontal number", 2,8))

    # Spacings
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 17px; font-weight: bold; ">Edge distance</p>'
    st.markdown(header, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:  
        edgeVertical = int(st.slider("Vertical edge (mm)", 10,80, step=10))
    with col2:  
        edgeHorizontal = int(st.slider("Horizontal edge (mm)", 10,80, step=10))

    # Loads
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 17px; font-weight: bold; ">Loading</p>'
    st.markdown(header, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:  
        forceShear = int(st.slider("Shear Force (kN)", 1,200, step = 10))
    with col2:
        xPosition = int(st.slider("Eccentricity (mm)", -timberWidth, timberWidth, 10, step = 10))


# ____________________calculation___________________________________
# __________________________________________________________________
try:  
    # Class
    class fastener:
        def __init__(self, name, x, y, area, rx, ry, rxy, alpha, ShearX, ShearY, ShearXY):
            self.name = name
            self.x = x
            self.y = int(y)
            self.area = area
            self.rx = rx
            self.ry = ry
            self.rxy = rxy
            self.alpha = alpha
            self.ShearX = ShearX
            self.ShearY = ShearY
            self.ShearXY = ShearXY

    # Initiation of lists
    xCordinates = []
    yCordinates = []
    fastenerList = []    # List that holds instances from fastener-class
    fastenerDict = defaultdict(list)
    productxList = []
    productyList = []
    rxyList =[]
    IcxList = []
    IcyList = []
    shearXList = []
    shearYList = []
    shearXYList = []

    # calculation of coordination of fasteners
    distanceVertical = ( timberHeight - 2 * edgeVertical ) / (noVertical-1)
    distanceHorizontal = ( timberWidth - 2 * edgeHorizontal ) / (noHorizontal-1)

    # Bolt Pattern Area
    area = round(pi*diameter**2 / 4,1)
    totalArea = int(area* noVertical * noHorizontal)

    # Cordinates of bolts
    xCoordinates = [(edgeHorizontal + i * distanceHorizontal) for i in range(noHorizontal)]
    yCoordinates = [(edgeVertical + i * distanceVertical) for i in range(noVertical)]

    ## all possible combinations
    xyCoordinates = list(product(xCoordinates, yCoordinates))
    numberFastener = len(xyCoordinates)

    ## x/y-cordinates split in lists
    xCordinatesList = [(xyCoordinates[i][0]) for i in range(len(xyCoordinates))]
    yCordinatesList = [(xyCoordinates[i][1]) for i in range(len(xyCoordinates))]

    # Initiating object
    for i in range(numberFastener):

        point = fastener(f"F{i}", xCordinatesList[i], yCordinatesList[i], area, None, None, None, None, None, None, None)
        fastenerList.append(point)
        productxi = fastenerList[i].x * fastenerList[i].area
        productyi = fastenerList[i].y * fastenerList[i].area
        productxList.append(productxi)
        productyList.append(productyi)

    # Centroid
    centroid_cx = round(sum(productxList) / totalArea,2)
    centroid_cy = round(sum(productyList) / totalArea,2)

    # Bolt Pattern Moments of Inertia
    for i in range(numberFastener):

        rxi = round(fastenerList[i].x - centroid_cx,1)    # x-distance to centroid
        ryi = round(fastenerList[i].y - centroid_cy,1)    # y-distance to centroid
        rxyi = round(sqrt(rxi**2 + ryi**2),1)    # xy-distance to centroid
        Icxi = rxi**2 * fastenerList[i].area    # centroidal moment of inertia about the X-axis
        Icyi = ryi**2 * fastenerList[i].area    # centroidal moment of inertia about the Y-axis

        setattr(fastenerList[i], "rx", rxi)
        setattr(fastenerList[i], "ry", ryi)
        setattr(fastenerList[i], "rxy", rxyi)
        IcxList.append(Icxi)
        IcyList.append(Icyi)
        rxyList.append(rxyi**2)

    Icx = int(sum(IcxList))    # centroidal moment of inertia about the X-axis
    Icy = int(sum(IcyList))    # centroidal moment of inertia about the Y-axis
    Icp = Icx + Icy    # polar moment of inertia

    # Moment
    M_cz = xPosition * forceShear

    # Shear Forces
    for i in range(numberFastener):

        ShearXY = M_cz * fastenerList[i].rxy * fastenerList[i].area / Icp
        ShearX = -fastenerList[i].ry * M_cz / Icp
        ShearY = fastenerList[i].rx * M_cz / Icp
        alpha = atan(ShearY/ShearX)

        setattr(fastenerList[i], "ShearX", round(ShearX,3))
        setattr(fastenerList[i], "ShearY", round(ShearY,3))
        setattr(fastenerList[i], "ShearXY", round(ShearXY, 3))
        setattr(fastenerList[i], "alpha", round(alpha * 180 / pi,1))

        shearXList.append(ShearX)
        shearYList.append(ShearY)
        shearXYList.append(ShearXY)

    # Bolt force arrows
    maxShearX = max(shearXList)
    maxShearY = max(shearYList)
    maxShearXY = max(shearXYList)

    shearXProp = [shearXi / maxShearX for shearXi in shearXList]
    shearYProp = [shearYi / maxShearY for shearYi in shearYList]
    shearXYProp = [shearXYi / maxShearXY for shearXYi in shearXYList]

    arrowLength = 30
    arrowListx = [arrowLength * shearXProp[i] for i in range(numberFastener)]
    arrowListy = [arrowLength * shearYProp[i] for i in range(numberFastener)]

    # Total reaction
    totalShearX = sum(shearXList)
    totalShearY = sum(shearYList)
    maxShearXYtotal = max([totalShearX, totalShearY])
    totalShearXProp = totalShearX / maxShearXYtotal * arrowLength
    totalShearYProp = totalShearY / maxShearXYtotal * arrowLength
    totalShearXY = max(shearXYList)
    theta = round((atan(totalShearY/totalShearX)),2)

    # Summary of lists
    fastenerList = fastenerList   # List with all call objects
    xCordinatesList = xCordinatesList  # List with x-coordinates
    yCordinatesList = yCordinatesList  # List with y-coordinates
    shearXList = shearXList    # List with x-reaction
    shearYList = shearYList   # List with y-reaction
    shearXYList = shearXYList   # List with xy-reaction
    shearXProp = shearXProp    # List with proportional value for x
    shearYProp = shearYProp   # List with proportional value for y
    shearXYProp = shearXYProp   # List with proportional value for xy
    arrowListx = arrowListx # List with arrow length for x
    arrowListy = arrowListy    # List with arrow length for y

    # Dictionary from class for table
    fastenerListDict = [fastenerList[i].__dict__ for i in range(numberFastener)]
    for d in fastenerListDict:
        for key, value in d.items():
            # Append each value to the list associated with the key
            fastenerDict[key].append(value)

    col1, col2 = st.columns(2)
    with col1:
        header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">Graph</p>'
        st.markdown(header, unsafe_allow_html=True)
    with col2:
        header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">Table</p>'
        st.markdown(header, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        options1 = st.radio("Bolt Force Distribution", ["Resultant Forces", "X/Y Forces"])
    with col2:
        options2 = st.radio("Resultant Forces ", ["Resultant Force", "X/Y Forces "])
    with col3:
        options3 = st.radio("Show text?", ["No", "Yes"])

    # _______________________Visualization______________________________
    # __________________________________________________________________
    col1, col2 = st.columns(2)
    with col1:

        # Steel shape
        xList = [0,timberWidth,timberWidth,0, 0]
        yList = [0,0,timberHeight,timberHeight,0]
        fillColor = "lightgrey"
        lineColor = "darkgrey"
        fig = go.Figure(plotly_go_scatter_shape(xList, yList, fillColor, lineColor))

        for n,i in enumerate(xyCoordinates):

            x = i[0]
            y = i[1]

            # bolt markers
            go_scatter = plotly_go_scatter_marker([x], [y], diameter, "black")
            fig.add_trace(go_scatter)


        # Centroid text
        go_scatter = plotly_go_scatter_text([centroid_cx], [centroid_cy], "C", None, None, None, "top right")
        fig.add_trace(go_scatter)

        # Centroid marker
        go_scatter = plotly_go_scatter_marker([centroid_cx], [centroid_cy], diameter/2, "grey")
        fig.add_trace(go_scatter)

        # Moment text
        go_scatter = plotly_go_scatter_text([timberWidth + 50], [timberHeight / 2 + 30], f"Mc = {M_cz/ 1000} kNm", None, 20, "black", "middle right")
        fig.add_trace(go_scatter)

        # Resultant text
        go_scatter = plotly_go_scatter_text([timberWidth + 50], [timberHeight / 2 - 0], f"R = {round(totalShearXY,2)} kN", None, 20, "black", "middle right")
        fig.add_trace(go_scatter)

        # theta text
        go_scatter = plotly_go_scatter_text([timberWidth + 50], [timberHeight / 2 - 30], f"θ = {round(theta * 180 / pi,1)} °", None, 20, "black", "middle right")
        fig.add_trace(go_scatter)
                
        # Force arrow
        x = xPosition + timberWidth / 2
        y = timberHeight
        plotly_add_arrow(fig, x, y, 0, -50, 2, 1, "red")

        # Bolt force arrow
        for i in range(numberFastener):
            x = fastenerList[i].x
            y = fastenerList[i].y
            ax = arrowListx[i]
            ay = arrowListy[i]

            shearXi = round(fastenerList[i].ShearX,2)
            shearYi = round(fastenerList[i].ShearY,2)
            shearXYi = fastenerList[i].ShearXY

            if options1 == "X/Y Forces":
                plotly_add_arrow(fig, x, y, ax, 0, 2, 1, "red")
                plotly_add_arrow(fig, x, y, 0, ay, 2, 1, "red")
                text1 = f'{shearXi}/{shearYi} kN'

            elif options1 == "Resultant Forces":
                plotly_add_arrow(fig, x, y, ax, ay, 2, 1, "red")
                text1 = f'{round(shearXYi,2)} kN'
            
            else:
                plotly_add_arrow(fig, x, y, ax, ay, 2, 1, "red")

            if options2 == "X/Y Forces ":
                plotly_add_arrow(fig, timberWidth / 2, timberHeight / 2, totalShearXProp, 0, 2, 1, "blue")
                plotly_add_arrow(fig, timberWidth / 2, timberHeight / 2, 0, totalShearYProp, 2, 1, "blue")
                text2 = f'{round(totalShearX,2)}/{round(totalShearY,2)} kN'
                
            elif options2 == "Resultant Force":
                plotly_add_arrow(fig, timberWidth / 2, timberHeight / 2, totalShearXProp, totalShearYProp, 2, 1, "blue")
                text2 = f'{round(totalShearXY,2)} kN'

            if options3 == "Yes":
                # Force text
                go_scatter = plotly_go_scatter_text([x], [y+diameter], text1, None, None, "black", "top center")
                fig.add_trace(go_scatter)

            else:
                xxx = 1

        if options3 == "Yes":

            # Resultant text
            go_scatter = plotly_go_scatter_text([timberWidth / 2], [timberHeight / 2 - 15], text2, None, None, "black", "top center")
            fig.add_trace(go_scatter)
        else:
            xxx = 1

        # Force arrow text
        go_scatter = plotly_go_scatter_text([xPosition + timberWidth / 2], [y + 80], f'{forceShear}kN', None, None, "black", "top center")
        fig.add_trace(go_scatter)

        fig.update_layout(
            autosize=False,
            width=timberWidth + 500,
            height=timberHeight + 300,
            uirevision='static',  # Disable zoom functionality
            showlegend=False)

        # Set the aspect ratio to be equal
        fig.update_layout(
            xaxis=dict(scaleanchor="y", scaleratio=1,fixedrange=True, visible=False),
            yaxis=dict(scaleanchor="x", scaleratio=1, fixedrange=True, visible=False),
            uirevision='static',
            plot_bgcolor = "white")  # Disable zoom functionality

        # Hide the axis
        fig.update_xaxes(showline=False, showgrid=False, zeroline=False)
        fig.update_yaxes(showline=False, showgrid=False, zeroline=False)

        st.write(fig)

    # Table
    with col2:

        st.write("")
        st.write("")
        st.write("")
        st.write("")

        headerList = [key for key in fastenerDict.keys()]
        valuesList = [value for value in fastenerDict.values()]

        table_trace = go.Table(
            header=dict(values=headerList,
                        line_color='lightgrey',
                        height=40),
            cells=dict(values=valuesList,
                    line_color='lightgrey',
                    align='left',
                    height=30))

        # Create figure
        table = go.Figure(data=[table_trace])
        table.update_layout(width = 700, height = timberHeight + 300)
        st.write(table)

    # __________________________Report__________________________________
    # __________________________________________________________________

    with st.expander("Report"):

        # chapter 1: calculate relevant properties   
        st.latex(r"\textbf{Calculate relevant pattern properties.}")

        # area
        st.latex(r"\text{Area}")
        st.latex(r'''A = ''' + str(totalArea) + r''' mm2''') 

        # centroid
        st.latex(r"\text{Centroid}")

        st.latex(r'''x_{c} = ''' + str(centroid_cx) + r''' mm''') 
        st.latex(r'''y_{c} = ''' + str(centroid_cy) + r''' mm''') 

        # moments of inertia
        st.latex(r"\text{Moments of inertia}")
        st.latex(r'''I_{cx} = ''' + str(Icx) + r''' mm^4''')
        st.latex(r'''I_{cy} = ''' + str(Icy) + r''' mm^4''')
        st.latex(r'''I_{cp} = ''' + str(Icp) + r''' mm^4''')

        # shear forces
        st.latex(r"\text{Shear Forces}")
        st.latex(r'''P_{xtotal} = ''' + str(round(totalShearX,2)) + r''' kN''')
        st.latex(r'''P_{ytotal} = ''' + str(round(totalShearY,2)) + r''' kN''')
        st.latex(r'''P_{resultant} = ''' + str(round(totalShearXY,2)) + r''' kN''')
        st.latex(r'''\theta = ''' + str(round(theta * 180 / pi,2)) + r'''deg''')

except:
    st.warning("Some error happened. Change input.")
