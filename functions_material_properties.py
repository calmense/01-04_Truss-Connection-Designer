# ================ MATERIAL PROPERTIES ============================
# =================================================================

import pandas as pd

# Function to get steel tensile strength
def getTensileStrength(steelGrade):

    # Define steel parameters
    steel_grades = ["S235", "S275", "S355"]
    tensile_strengths = [360, 430, 490]
    yield_strengths = [235, 275, 355]

    # Find the index of the grade
    index = steel_grades.index(steelGrade)

    # Access the tensile strength from the list
    f_u = tensile_strengths[index]
    f_y = yield_strengths[index]

    return f_u, f_y

# Function to get timber density
def getTimberDensity(grade):

    # Define timber parameters
    timber_grades = ['GL24h', 'GL24c', 'GL28h','GL28c', 'GL32h', 'GL32c']
    timber_densities = [380, 350, 410, 380, 430, 410]

    # Find the index of the grade
    index = timber_grades.index(grade)

    # Access the density from the list
    rho_k = timber_densities[index]

    return rho_k

# Function to get modification factor
def get_kmod(serviceClass, loadDurationCLass):

    # Define service class, load duration class, and modification factor
    df_dict = {'permanent': [0.6, 0.6, 0.5], 
               'long-term': [0.7, 0.7, 0.55], 
               'medium-term': [0.8, 0.8, 0.65], 
               'short-term': [0.9, 0.9, 0.7], 
               'instantaneous': [1.1, 1.1, 0.9]}
    df = pd.DataFrame(data=df_dict, index=[1, 2, 3])
    
    # Look up the modification factor
    k_mod = float(df.at[serviceClass, loadDurationCLass])
    
    # Calculate gamma and chi
    gamma = 1.3
    chi = k_mod/gamma
    
    return k_mod, gamma, chi

# Timber properties
L_glulam_classes = []

# Define lists for timber properties
# DIN EN 14080
L_grades = ["GL20c", "GL22c", "GL24c", "GL26c", "GL28c", "GL30c", "GL32c", "GL20h", "GL22h", "GL24h", "GL26h", "GL28h", "GL30h", "GL32h"]
L_rhok = [355, 355, 365, 385, 390, 390, 400, 340, 370, 385, 405, 425, 430, 440]
L_fmk = [20, 22, 24, 26, 28, 30, 32, 20, 22, 24, 26, 28, 30, 32]
L_ft0k = [15, 16, 17, 19, 19.5, 19.5, 19.5, 16, 17.6, 19.2, 20.8, 22.3, 24, 25.6]
L_ft90k = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
L_fc0k = [18.5, 20, 21.5, 23.5, 24, 24.5, 24.5, 20, 22, 24, 26, 28, 30, 32]
L_c90k = [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5]
L_fvk = [3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5]
L_E0mean = [10400, 10400, 11000, 12000, 12500, 13000, 13500, 8400, 10500, 11500, 12100, 12600, 13600, 14200]
L_E05 = [8600, 8600, 9100, 10000, 10400, 10800, 11200, 7000, 8800, 9860, 10100, 10500, 11300, 11800]
L_G05 = [540, 540, 540, 540, 540, 540, 540, 540, 540, 540, 540, 540, 540, 540]

# Class for glulam properties
class Glulam:
    def __init__(self, name, rho_k, f_mk, f_c0k, f_t0k, f_t90k, f_c90k, f_vk, E0mean, E05, G05):
        self.name = name
        self.rho_k = rho_k
        self.f_mk = f_mk
        self.f_t0k = f_t0k
        self.f_t90k = f_t90k
        self.f_c0k = f_c0k
        self.f_c90k = f_c90k
        self.f_vk = f_vk
        self.E0mean = E0mean
        self.E05 = E05
        self.G05 = G05

# Instantiate objects using a loop
for i in range(len(L_grades)):
    L_glulam_classes.append(Glulam(L_grades[i], L_rhok[i], L_fmk[i], L_fc0k[i], L_ft0k[i], L_ft90k[i], L_c90k[i], L_fvk[i], L_E0mean[i], L_E05[i], L_G05[i]))

# Function to get glulam properties
def get_glulam_properties(grade):
    # Find index of the grade
    timber_index = L_grades.index(grade)
    
    # Retrieve glulam class
    glulam_class = L_glulam_classes[timber_index]
    
    # Retrieve timber properties
    name = L_glulam_classes[timber_index].name 
    rho_k = L_glulam_classes[timber_index].rho_k 
    f_myk = L_glulam_classes[timber_index].f_mk 
    f_t0k = L_glulam_classes[timber_index].f_t0k    
    f_t90k = L_glulam_classes[timber_index].f_t90k    
    f_c0k = L_glulam_classes[timber_index].f_c0k    
    f_c90k = L_glulam_classes[timber_index].f_c90k  
    f_vk = L_glulam_classes[timber_index].f_vk   
    E_0mean = L_glulam_classes[timber_index].E0mean    
    E_05 = L_glulam_classes[timber_index].E05   
    G_05 = L_glulam_classes[timber_index].G05 
    
    return glulam_class, name, rho_k, f_myk, f_c0k, f_t0k, f_t90k, f_c90k, f_vk, E_0mean, E_05, G_05

# Retrieve glulam properties for a specific grade
glulam_class, name, rho_k, f_myk, f_c0k, f_t0k, f_t90k, f_c90k, f_vk, E_0mean, E_05, G_05 = get_glulam_properties("GL24h")

