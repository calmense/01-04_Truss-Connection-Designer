# ============= FUNCTION ==========================================
# _____________ Checks ____________________________________________

# Import necessary functions and modules
from functions_material_properties import *  # Importing functions for material properties (assuming they are defined elsewhere)
from math import sqrt  # Import square root function
import streamlit as st  # Import streamlit for creating web applications



# Function to check shear member utilization
def tensionMemberCheck(thickness, height, noPerpendicular, diameter, tensionForce, timberGrade, noSheet, chi, thicknessSheet):
    # Get glulam properties
    glulam_class, name, rho_k, f_myk, f_c0k, f_t0k, f_t90k, f_c90k, f_vk, E_0mean, E_05, G_05 = get_glulam_properties(timberGrade)
    
    # Calculate design shear resistance
    k_t = 0.4
    f_td = round(f_t0k * chi * k_t, 2)

    # Effective length factor
    b_ef = thickness - thicknessSheet * 0.5 * min(noSheet, 2)

    # Calculate net area
    A_net = round(height * b_ef - noPerpendicular * diameter * b_ef, 2)

    # Calculate force
    tensionForce = round(tensionForce / 2, 1)

    # Calculate stress
    sigma_t0d = round((tensionForce) / A_net * 1000, 2)
    
    # Calculate utilization ratio
    eta = round(sigma_t0d / f_td , 2)
    
    return A_net, f_t0k, f_td, tensionForce, sigma_t0d, round(b_ef, 2), eta



# Function to check shear member utilization
def compressionMemberCheck(thickness, height, noPerpendicular, diameter, compressionForce, timberGrade, noSheet, chi, thicknessSheet):
    # Get glulam properties
    glulam_class, name, rho_k, f_myk, f_c0k, f_t0k, f_t90k, f_c90k, f_vk, E_0mean, E_05, G_05 = get_glulam_properties(timberGrade)
    
    # Calculate design shear resistance
    f_cd = round(f_c0k * chi, 2)

    # Effective length factor
    k_t = 1
    b_ef = thickness - thicknessSheet * 0.5 * min(noSheet, 2)

    # Calculate net area
    A_net = height * b_ef

    # Calculate force
    compressionForce = abs(round(compressionForce / 2, 1))
    
    # Calculate shear stress
    sigma_c0d = round(compressionForce / A_net * 1000, 2)
    
    # Calculate utilization ratio
    eta = round(sigma_c0d / f_cd , 2)
    
    return A_net, f_c0k, f_cd, compressionForce, sigma_c0d, round(b_ef, 2), eta




# Function to check shear block failure
def blockFailureCheckAxial(steelGrade, noPerp, noAxial, diameter, thickness, distancesFinal, axialForce, noSheet):

    d0 = diameter + 0.6
    thickness = thickness
    # Get tensile and yield strength of steel
    f_u, f_y = getTensileStrength(steelGrade)
    
    # Calculate lengths
    a1 = distancesFinal[0][0]
    a2 = distancesFinal[0][1]
    e1 = distancesFinal[0][4]

    Lh = a2 * (noPerp - 1)
    Lv = a1 * (noAxial - 1) + e1

    # Calculate effective areas
    Ant = (Lh - (noPerp - 1) * d0) * thickness * noSheet
    Anv = 2 * (Lv - (noAxial - 0.5) * d0 ) * thickness * noSheet
    
    # Calculate design shear resistance
    V_eff1Rd = round(((f_u * Ant) / 1.25 + (f_y * Anv) / (sqrt(3) * 1)) / 1000)
    
    # Calculate utilization ratio
    eta = round(abs(axialForce) / V_eff1Rd, 2)

    Ant = round(Ant * 0.1**2, 1)
    Anv = round(Anv * 0.1**2, 1)

    return Lh, Lv, Ant, Anv, V_eff1Rd, eta


 # calculate max eta
def getEtaMax(ClassList):

    fastenerCheckList = []
    tensionMemberCheckList = []
    compressionMemberList = []
    axialBlockFailureList = []

    for beam in ClassList:

        # checks
        fastenerCheckList.append(beam.fastenerCheck)
        tensionMemberCheckList.append(beam.tensionMemberCheck )
        compressionMemberList.append(beam.compressionMemberCheck )
        axialBlockFailureList.append(beam.axialBlockFailureCheck )

    fastenerCheckMax = max(fastenerCheckList)
    tensionMemberCheckMax = max(tensionMemberCheckList)
    compressionMemberMax = max(compressionMemberList)
    axialBlockFailureMax = max(axialBlockFailureList)

    fastenerCheckMaxIndex = fastenerCheckList.index(fastenerCheckMax)
    tensionMemberCheckMaxIndex = tensionMemberCheckList.index(tensionMemberCheckMax)
    compressionMemberMaxIndex = compressionMemberList.index(compressionMemberMax)
    axialBlockFailureMaxIndex = axialBlockFailureList.index(axialBlockFailureMax)

    return fastenerCheckMax, tensionMemberCheckMax, compressionMemberMax, axialBlockFailureMax, fastenerCheckMaxIndex, tensionMemberCheckMaxIndex, compressionMemberMaxIndex, axialBlockFailureMaxIndex
