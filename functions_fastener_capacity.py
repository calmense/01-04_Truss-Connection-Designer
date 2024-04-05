from functions_material_properties import *
from math import *
import streamlit as st

def characteristicValues(diameter, timberGrade, strengthClass, angle):

    # Get the tensile strength of the timber
    f_ub, f_y = getTensileStrength(strengthClass)
    
    # Calculate the characteristic moment capacity
    M_yrk = 0.3 * f_ub * diameter ** 2.6
    
    # Get the density of the timber
    rho_k = getTimberDensity(timberGrade)
    
    # Calculate the characteristic value of the compression strength
    f_h0k = 0.082 * (1 - 0.01 * diameter) * rho_k
    
    # Calculate the angle correction factor
    k_90 = 1.35 + 0.015 * diameter
    
    # Calculate the characteristic value of the compression strength at the given angle
    f_halphak = f_h0k / (k_90 * sin(radians(angle))**2 + cos(radians(angle))**2)
    
    # Determine the compression strength based on the angle
    f_hk = f_h0k if angle == 0 else f_halphak
    
    # Return the tensile strength, moment capacity, and compression strength
    return f_ub, round(M_yrk), round(f_h0k,1), round(f_halphak,1)


def shearCapacity(diameter, thickness, timberGrade, strengthClass, angle, chi):

    # Get characteristic values
    f_ub, M_yrk, f_h0k, f_halphak = characteristicValues(diameter, timberGrade, strengthClass, angle)

    # Calculate the shear capacity based on different failure modes
    # 1 sheet
    F_vrkf = round(f_h0k * thickness * diameter / 1000, 1)
    F_vrkg = round(f_h0k * thickness * diameter * ( sqrt( 2 + (4 * M_yrk) / (f_h0k * diameter * thickness**2)) - 1) / 1000, 1)
    F_vrkh = round(2.3 * sqrt(  M_yrk * f_h0k * diameter) / 1000, 1)

    # 2 sheets
    F_vrkl = round(f_h0k * thickness * diameter / 1000, 1)
    F_vrkm = F_vrkh

    # Select the minimum shear capacity from the calculated values
    F_vrk1 = min ( F_vrkf, F_vrkg, F_vrkh )
    F_vrk2 = min ( F_vrkf, F_vrkh, F_vrkl, F_vrkm )
    
    F_vrd1 = round(F_vrk1 * chi, 1)
    F_vrd2 = round(F_vrk2 * chi, 1)

    F_vrd = min(F_vrd1, F_vrd2)

    # Return the shear capacity in kilonewtons (kN)
    return F_vrd, F_vrd1, F_vrd2, F_vrk1, F_vrk2, F_vrkf, F_vrkg, F_vrkh, F_vrkl, F_vrkm