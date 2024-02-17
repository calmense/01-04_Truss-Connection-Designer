# Schraubenbemessungsprogramm: Webapp mit Streamlit - Axial- und Schertragfähigkeit von Würth Vollgewindeschrauben
# Bibliotheken
from math import pi, sqrt, cos, sin, atan
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from itertools import product

# from würth_screws_functions import get_length, ec5_87_tragfähigkeit_vg, get_min_distances_axial, get_min_distances_shear

# HTML Einstellungen
st.set_page_config(layout="wide")
st.markdown("""<style>
[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 500px;}
[data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 500px;margin-left: -500px;}
footer:after{
    content:"Berliner Hochschule für Technik (BHT) | Konstruktiver Hoch- und Ingenieurbau (M.Eng.) | \
    Ingenieurholzbau | Prof. Dr. Jens Kickler | Cal Mense 914553";
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

# classes
class fastener:
    def __init__(self, name, x, y, area, rx, ry, rxy, alpha, ShearX, ShearY, ShearXY):
        self.name = name
        self.x = x
        self.y = y
        self.area = area
        self.rx = rx
        self.ry = ry
        self.rxy = rxy
        self.alpha = alpha
        self.ShearX = ShearX
        self.ShearY = ShearY
        self.ShearXY = ShearXY

# header
st.write("")
st.write("")
st.write("")
header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 25px; font-weight: bold; ">In-Plane Eccentric Shear Load</p>'
st.markdown(header, unsafe_allow_html=True)
st.latex(r"\textbf{Input Parameters}")

# input parameter
# timber parameter
col1, col2, col3, col4 = st.columns(4)
with col1:  
    timberWidth = int(st.text_input("timber width", 200))
with col2:  
    timberHeight = int(st.text_input("timber height", 400))

# spacing
col1, col2, col3, col4 = st.columns(4)
with col1:  
    diameter = st.selectbox("diameter (mm)", [6,8,10])
with col2:  
    edgeVertical = int(st.text_input("vertical edge distance", 40))
with col3:  
    edgeHorizontal = int(st.text_input("horizontal edge distance", 40))

# bolt parameter
col1, col2 = st.columns(2)
with col1:  
    noVertical = int(st.slider("vertical number", 2,8))
with col2:
    noHorizontal = int(st.slider("horizontal number", 2,8))

# load
col1, col2 = st.columns(2)
with col1:  
    forceShear = int(st.slider("Shear Force (kN)", 2,8))
with col2:
    xPosition = int(st.slider("horizontal position", 0,timberWidth))

# calculations
# calculation of coordination of fasteners
distanceVertical = ( timberHeight - 2 * edgeVertical ) / (noVertical-1)
distanceHorizontal = ( timberWidth - 2 * edgeHorizontal ) / (noHorizontal-1)

# area
area = pi*diameter**2 / 4 

# coordinates of fasteners
xCordinates = []
yCordinates = []
fastenerList = []

for i in range(noHorizontal):
    x = edgeHorizontal + i * distanceHorizontal
    xCordinates.append(int(x))

for j in range(noVertical):
    y = edgeVertical + j * distanceVertical
    yCordinates.append(int(y))

# resulting list with coordinates
combined_lists = list(product(xCordinates, yCordinates))    

# add items to class
for i in range(len(combined_lists)):
    point = fastener(f"fastener {i}", combined_lists[i][0], combined_lists[i][1], area, None, None, None, None, None, None, None)
    fastenerList.append(point)

with st.expander("calculation"):
    # chapter 1: calculate relevant properties   
    st.latex(r"\textbf{Calculate relevant pattern properties.}")

    # area
    st.latex(r"\text{Area}")
    totalArea = int(area* noVertical * noHorizontal)
    st.latex(r'''A = ''' + str(totalArea) + r''' mm2''') 

    # centroid
    st.latex(r"\text{Centroid}")
    productxList = []
    productyList = []

    for i in range(len(combined_lists)):
        productxi = fastenerList[i].x * fastenerList[i].area
        productxList.append(productxi)

        productyi = fastenerList[i].y * fastenerList[i].area
        productyList.append(productyi)

    centroid_cx = round(sum(productxList) / totalArea,2)
    centroid_cy = round(sum(productyList) / totalArea,2)

    st.latex(r'''x_{c} = ''' + str(centroid_cx) + r''' mm''') 
    st.latex(r'''y_{c} = ''' + str(centroid_cy) + r''' mm''') 

    # moments of inertia
    st.latex(r"\text{Moments of inertia}")

    IcxList = []
    IcyList = []

    # add items to class
    for i in range(len(combined_lists)):
        rxi = fastenerList[i].x - centroid_cx
        ryi = fastenerList[i].y - centroid_cy
        rxyi = sqrt(rxi**2 + ryi**2)
        alpha = atan(ryi/rxi)
        setattr(fastenerList[i], "rx", rxi)
        setattr(fastenerList[i], "ry", ryi)
        setattr(fastenerList[i], "rxy", rxyi)
        setattr(fastenerList[i], "alpha", alpha)
        Icxi = rxi**2 * fastenerList[i].area
        Icyi = ryi**2 * fastenerList[i].area

        IcxList.append(Icxi)
        IcyList.append(Icyi)

    Icx = int(sum(IcxList))
    Icy = int(sum(IcyList))
    Icp = Icx + Icy

    st.latex(r'''I_{cx} = ''' + str(Icx) + r''' mm^4''')
    st.latex(r'''I_{cy} = ''' + str(Icy) + r''' mm^4''')
    st.latex(r'''I_{cp} = ''' + str(Icp) + r''' mm^4''')

    #st.latex(r"\textbf{2. Translate all applied forces and moments to the centroid of the pattern.}")
    #st.latex(r"\textbf{3. Calculate axial and shear loads acting on individual bolted joints in the pattern.}")

    leverArm = -(timberWidth/2 -xPosition)
    M_cz = leverArm * forceShear

    # add items to class
    for i in range(len(combined_lists)):
        ShearXY = round(M_cz * fastenerList[i].rxy * fastenerList[i].area / Icp,2)
        ShearX = round(ShearXY*sin(alpha),2)
        ShearY = round(-ShearXY*cos(alpha),2)

        ShearX = round(fastenerList[i].area * M_cz * fastenerList[i].rx / Icp,2)
        ShearY = round(fastenerList[i].area * M_cz * fastenerList[i].ry / Icp,2)

        setattr(fastenerList[i], "ShearX", ShearX)
        setattr(fastenerList[i], "ShearY", ShearY)
        setattr(fastenerList[i], "ShearXY", ShearXY)

        #st.write(ShearX)
        #st.write(ShearY)

# plotly
fig = go.Figure(go.Scatter(x=[0,timberWidth,timberWidth,0, 0], 
                           y=[0,0,timberHeight,timberHeight,0], 
                           fillcolor='lightgrey',  
                           line=dict(color='darkgrey'),
                           mode="lines",
                           fill="toself"))

annotationX = []
annotationY = []
annotationXY = []

xCoord = []
yCoord = []
shearX = []
shearY = []
shearXY = []

for n,i in enumerate(combined_lists):
    x = i[0]
    y = i[1]

    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers",marker=dict(size=diameter*2, color="black")))

shearList = ["r"]
selection = "r"
indexSelection = shearList.index(selection)
Fx = shearList[indexSelection]

for n,i in enumerate(combined_lists):
    x = i[0]
    y = i[1]

    shearXi = fastenerList[n].ShearX
    shearYi = fastenerList[n].ShearY
    shearXYi = fastenerList[n].ShearXY

    selectionList = [shearXi, shearYi, shearXYi]
    shear = selectionList[indexSelection]

    fig.add_annotation(
            x=x,
            y=y + 2 * diameter,
            text=f'{Fx}={shear}',
            showarrow=False,
            arrowhead=2,
            arrowsize=1)
    
    fig.add_trace(go.Scatter(x=[x+shearXi*200, x], y=[y+shearYi*200, y],
            marker= dict(size=10,symbol= "arrow-bar-up", angleref="previous", color = "black")))

    #st.write("name="+str(fastenerList[n].name))
    #st.write("rx="+str(fastenerList[n].rx))
    #st.write("ry="+str(fastenerList[n].ry))
    #st.write("shearXi="+str(fastenerList[n].name))
    #st.write("shearXi="+str(shearXi))
    #st.write("shearYi="+str(shearYi))
    
# Add an arrow annotation
fig.add_annotation(
    x=xPosition,  # X-coordinate of the arrow tail
    y=timberHeight,  # Y-coordinate of the arrow tail
    ax=0,  # X-coordinate of the arrowhead
    ay=-50,  # Y-coordinate of the arrowhead
    arrowhead=2,  # Arrowhead style (2 is an arrow)
    arrowsize=1,  # Arrowhead size
    arrowcolor='red')

fig.update_layout(
    autosize=False,
    width=timberWidth + 200,
    height=timberHeight + 300,
    uirevision='static',  # Disable zoom functionality
    showlegend=False)

# Set the aspect ratio to be equal
fig.update_layout(
    xaxis=dict(scaleanchor="y", scaleratio=1,fixedrange=True),
    yaxis=dict(scaleanchor="x", scaleratio=1, fixedrange=True),
    uirevision='static')  # Disable zoom functionality

# Hide the axis
fig.update_xaxes(showline=False, showgrid=False, zeroline=False)
fig.update_yaxes(showline=False, showgrid=False, zeroline=False)



# Create buttons
#button_on = dict(label='Show Annotations', method='relayout', args=['annotationX', annotationX])

# Add buttons to toggle annotations
#fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[button_on])])


st.write(fig)