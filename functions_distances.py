# ============= FUNCTION ==========================================
# _____________ Distances _________________________________________

import math  # Import math module for mathematical functions
import pandas as pd  # Import pandas for data manipulation
import streamlit as st  # Import streamlit for creating web applications
from functions_material_properties import *

# Function to calculate minimum distances between bolts for timber
def calcMinDistancesTimber(diameter, alpha):
    # Calculate minimum distances based on given formulae
    a_1 = (3 + 2 * abs(math.cos(alpha))) * diameter
    a_2 = 3 * diameter
    a_3t = max(7 * diameter, 80)
    a_3c = max(diameter * abs(math.sin(alpha)), 3 * diameter)
    a_4t = max((2 + 2 * math.sin(alpha)) * diameter , 3 * diameter)
    a_4c = 3 * diameter

    # Round the calculated values and return as a list
    return [round(a_1), round(a_2), round(a_3t), round(a_3c), round(a_4t), round(a_4c)]

# Function to calculate effective number of bolts
def effectiveNumber(n_row, a_1, diameter):
    # Calculate effective number based on given formula
    n_ef = n_row**0.9
    n_ef = min (n_row, n_row ** (0.9) * (a_1 / (13 * diameter)) ** (1/4)) 

    return round(n_ef, 2)

# Function to calculate minimum distances between bolts for steel
def calcMinDistancesSteel(diameter):
    diameter = diameter + 0.6
    # Calculate minimum distances based on given formula
    e_1 = 3 * diameter
    e_2 = 1.5 * diameter
    p_1 = 3.75 * diameter
    p_2 = 3 * diameter

    # Round the calculated values and return as a list
    return [round(e_1), round(e_2), round(p_1), round(p_2)]

def roundToBase(x, base):
    return base * round(float(x) / base)

def calcMaxDistances(minDistancesListTimber, minDistancesListSteel, base):

    a1 = roundToBase(max(minDistancesListTimber[0], minDistancesListSteel[2]), base)
    a1 = max(40, 50)
    a2 = roundToBase(max(minDistancesListTimber[1], minDistancesListSteel[3]), base)
    a3t = roundToBase(minDistancesListTimber[2], base)
    a3c = roundToBase(minDistancesListTimber[3], base)
    a3 = max(a3t, a3c) * 2
    a4t = roundToBase(max(minDistancesListTimber[4], minDistancesListSteel[1]), base)
    a4c = roundToBase(max(minDistancesListTimber[5], minDistancesListSteel[1]), base)
    a4 = max(a4t, a4c) 
    e1 = roundToBase(minDistancesListSteel[0], base)

    distancesListRequired = [a1, a2, a3, a4, e1]

    return distancesListRequired
