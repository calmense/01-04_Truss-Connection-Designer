# Schraubenbemessungsprogramm: Webapp mit Streamlit - Axial- und Schertragfähigkeit von Würth Vollgewindeschrauben
# Bibliotheken
from math import pi, sqrt, cos, sin, atan, isnan
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from itertools import product
from functions_plotly import *
from functions_distances import *
from functions_material_properties import *
from functions_force_distribution import *
from functions_fastener_capacity import *
from functions_member_checks import *
from classes import *
from report import *



# HTML Einstellungen
st.set_page_config(page_title="Timber Connection Designer", layout="wide")
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
col1, col2 = st.columns(2)
with col1: 
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 40px; font-weight: bold; ">Truss Joint Designer</p>'
    st.markdown(header, unsafe_allow_html=True)
with col2: 
    st.image("awatif.png")



# ================ SIDEBAR ========================================
# =================================================================

with st.sidebar:

    # Input parameter
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">Global Parameters</p>'
    st.markdown(header, unsafe_allow_html=True)

    # Service Class
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 17px; font-weight: bold; ">Basic</p>'
    st.markdown(header, unsafe_allow_html=True)
    code = st.selectbox("Design Standard", ["DIN EN 1995: 2013"])

    # Service Class
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 17px; font-weight: bold; ">Load</p>'
    st.markdown(header, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:  
        serviceClass = st.selectbox("Service Class", [1, 2, 3])
    with col2: 
        loadDurationCLass = st.selectbox("Load Duration Class", ['permanent', 'long-term', 'medium-term','short-term', 'instantaneous'])

    # Timber
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 17px; font-weight: bold; ">Timber</p>'
    st.markdown(header, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:  
        timber = st.selectbox("Timber", ["Glulam", "Soft Wood"])
    with col2: 
        timberGrade = st.selectbox("Grade", ['GL24h', 'GL24c', 'GL28h','GL28c', 'GL32h', 'GL32c'])

    # Fastener
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 17px; font-weight: bold; ">Fastener</p>'
    st.markdown(header, unsafe_allow_html=True)
    st.write("Type: Dowel")

    col1, col2 = st.columns(2)
    with col1: 
        fastenerGrade = st.selectbox("Grade", ["S235", "S275", "S355"])
    with col2: 
        diameter = int(st.text_input("Diameter [mm]", 8))

    # Sheet
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 17px; font-weight: bold; ">Metal Sheet</p>'
    st.markdown(header, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: 
        sheetGrade = st.selectbox("Grade ", ["S235", "S275", "S355"])
    with col2: 
        sheetThickness = int(st.text_input("Thickness [mm]", 5))

    col1, col2 = st.columns(2)
    with col1: 
        sheetNo = st.selectbox("Number of sheets", [1, 2])


# ================ TABLE ==========================================
# =================================================================

# input editable table
df = pd.DataFrame([
    {"Beam": 1, "Height": 300, "Width": 300, "Angle": 0, "Axial Force": -87, "No Axial": 2, "No Perp": 10, "a1": 30, "a2": 24, "a3": 80, "a4": 42},
    {"Beam": 2, "Height": 200, "Width": 200, "Angle": 45, "Axial Force": -87, "No Axial": 2, "No Perp": 6, "a1": 40, "a2": 29, "a3": 80, "a4": 28},
    {"Beam": 3, "Height": 200, "Width": 200, "Angle": 90, "Axial Force": 70,  "No Axial": 3, "No Perp": 6, "a1": 40, "a2": 26, "a3": 80, "a4": 35},
    {"Beam": 4, "Height": 300, "Width": 300, "Angle": 180, "Axial Force": -70,  "No Axial": 3, "No Perp": 6, "a1": 40, "a2": 26, "a3": 80, "a4": 35},
    {"Beam": 5, "Height": 200, "Width": 200, "Angle": 135, "Axial Force": 70,  "No Axial": 3, "No Perp": 6, "a1": 40, "a2": 26, "a3": 80, "a4": 35},
])

edited_df = st.data_editor(df, hide_index=True, num_rows="dynamic") 
beams = [x for x in edited_df["Beam"]]
heights = [x for x in edited_df["Height"]]
widths = [x for x in edited_df["Width"]]
angles = [x for x in edited_df["Angle"]]
axialForce = [x for x in edited_df["Axial Force"]]
noAxial = [x for x in edited_df["No Axial"]]
noPerp = [x for x in edited_df["No Perp"]]

a1 = [x for x in edited_df["a1"]]
a2 = [x for x in edited_df["a2"]]
a3 = [x for x in edited_df["a3"]]
a4 = [x for x in edited_df["a4"]]


# ================ CALCULATION ====================================
# =================================================================
try:

    # initiating class object
    beamClassesList = [Beams(serviceClass, loadDurationCLass, beams[i], timberGrade, widths[i], heights[i], angles[i], axialForce[i], fastenerGrade, diameter, noAxial[i], noPerp[i], sheetGrade, sheetThickness, sheetNo) for i in range(len(beams))]

    fastenerMode = st.radio("Number of Fastener", ["Automatic", "Manual"])

    if fastenerMode == "Automatic":
        # calculate distances in steel and timber and maximum of it
        Beams.automaticDesign(beamClassesList)

    else:
        # calculate required fastener
        Beams.manualDesign(beamClassesList, a1, a2, a3, a4)


    # ================ VISUALIZATION ==================================
    # =================================================================

    drawSheets(beamClassesList)

    # ================ REPORT =========================================
    # =================================================================

    #show = st.radio("Show", ["Arrow", "Force", "Utilization", "Resistance", "Angle"])
    tabsList = [f"tab{beams[i]}" for i in range(len(beams))]
    tabsNames = [f"Beam {beams[i]}" for i in range(len(beams))]
    tabsList = st.tabs(tabsNames)

    for i, beam in enumerate(beamClassesList):

        with tabsList[i]:

            report(beamClassesList[i])

except:

    st.warning("Error")
       
