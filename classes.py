from math import * # Import math module for mathematical functions
from itertools import product
from functions_plotly import *
from functions_distances import *
from functions_material_properties import *
from functions_force_distribution import *
from functions_fastener_capacity import *
from functions_member_checks import *
from classes import *


class Beams:
    def __init__(self, serviceClass, loadDurationCLass, name, timberGrade, width, height, beamAngle, axialForce, fastenerGrade, fastenerDiameter, noAxial, noPerp, sheetGrade, sheetThickness, sheetNo):
        
        # basic
        self.serviceClass = serviceClass
        self.loadDurationCLass = loadDurationCLass
        self.k_mod = 0
        self.gamma = 0
        self.chi = 0

        self.name = name
        self.timberGrade = timberGrade 
        self.width = width
        self.thickness = width / (sheetNo + 1)
        self.height = height 
        self.beamAngle = beamAngle  

        # loading
        self.axialForce = axialForce 
        self.axialForceFastener = 0

        self.shearForceTotalFastener = []
        self.axialForceTotalFastener = []
        self.resultantForceTotalFastener = []
        self.resultantForceTotalFastenerSum = []

        # fastener
        self.fastenerGrade = fastenerGrade
        self.fastenerDiameter = fastenerDiameter
        self.noPerp = noPerp
        self.noAxial = noAxial
        self.noAxialEffective = 0
        self.noTotal = 0
        self.noTotalEffective = 0
        self.xCoordinates = []
        self.yCoordinates = []

        # fastener capacity
        self.F_vrdTotal = 0
        self.F_vrd = 0
        self.F_vrd1 = 0
        self.F_vrd2 = 0
        self.F_vrk1 = 0 
        self.F_vrk2 = 0 
        self.F_vrkf = 0 
        self.F_vrkg = 0 
        self.F_vrkh = 0 
        self.F_vrkl = 0 
        self.F_vrkm = 0 

        # fastener group
        self.centroid_cx = 0
        self.centroid_cy = 0
        self.Icp = 0
        self.fastenerAngle = 0
        self.shearXList = []
        self.shearYList = []
        self.shearXYList = []
        self.arrowListx = []
        self.arrowListy = []

        # fastener properties
        self.f_ub = 0
        self.M_yrk = 0
        self.f_h0k = 0
        self.f_halphak = 0

        # sheet
        self.sheetGrade = sheetGrade
        self.sheetThickness = sheetThickness
        self.sheetNo = sheetNo
        self.sheetLength = 0

        # distances
        self.distancesTimber = []
        self.distancesSteel = []
        self.distancesFinal = []

        # checks
        self.fastenerCheck = 0

        # tension member check
        self.Anet_axial = 0
        self.ft0k = 0
        self.ft0d = 0
        self.beft = 0
        self.tensionForce = 0
        self.sigmat0d = 0
        self.tensionMemberCheck = 0

        # compression member check
        self.fc0k = 0
        self.fc0d = 0 
        self.befc = 0
        self.compressionForce = 0
        self.sigmac0d = 0
        self.compressionMemberCheck = 0

        # axial block failure check
        self.Lh1 = 0
        self.Lv1 = 0
        self.Ant1 = 0
        self.Anv1 = 0
        self.Veff1Rd = 0
        self.axialBlockFailureCheck = 0


    # Function to get modification factor
    def getkmod(ClassList):

        # Define service class, load duration class, and modification factor
        df_dict = {'permanent': [0.6, 0.6, 0.5], 
                'long-term': [0.7, 0.7, 0.55], 
                'medium-term': [0.8, 0.8, 0.65], 
                'short-term': [0.9, 0.9, 0.7], 
                'instantaneous': [1.1, 1.1, 0.9]}
        df = pd.DataFrame(data=df_dict, index=[1, 2, 3])

        for beam in ClassList:
            
            # Look up the modification factor
            k_mod = float(df.at[beam.serviceClass, beam.loadDurationCLass])
            
            # Calculate gamma and chi
            gamma = 1.3
            chi = k_mod/gamma

            beam.k_mod = k_mod
            beam.gamma = gamma
            beam.chi = chi
            

    def getRequiredDistances(ClassList):

        for beam in ClassList:

            minDistancesListTimber = calcMinDistancesTimber(beam.fastenerDiameter, radians(0))
            minDistancesListSteel = calcMinDistancesSteel(beam.fastenerDiameter)
            distancesListRequired = calcMaxDistances(minDistancesListTimber, minDistancesListSteel, 1)

            beam.distancesTimber.append(minDistancesListTimber)
            beam.distancesSteel.append(minDistancesListSteel)
            beam.distancesFinal.append(distancesListRequired)


    def defineDistances(ClassList, a1, a2, a3, a4):

        for n, beam in enumerate(ClassList):

            e1 = roundToBase(3 * (beam.fastenerDiameter + 0.6), 1)
            distancesFinal = [a1[n], a2[n], a3[n], a4[n], e1]
            minDistancesListTimber = calcMinDistancesTimber(beam.fastenerDiameter, radians(0))
            minDistancesListSteel = calcMinDistancesSteel(beam.fastenerDiameter)

            beam.distancesFinal.append(distancesFinal)
            beam.distancesTimber.append(minDistancesListTimber)
            beam.distancesSteel.append(minDistancesListSteel)


    def calcFastenerProperties(ClassList):

        for beam in ClassList:

            f_ub, M_yrk, f_h0k, f_halphak = characteristicValues(beam.fastenerDiameter, beam.timberGrade, beam.fastenerGrade, 0)
            beam.f_ub = f_ub
            beam.M_yrk = M_yrk
            beam.f_h0k = f_h0k
            beam.f_halphak = f_halphak


    # initial assumption with shear and axial load angle
    def calcFastenerCapacity(ClassList):

        for beam in ClassList:
            
            F_vrd, F_vrd1, F_vrd2, F_vrk1, F_vrk2, F_vrkf, F_vrkg, F_vrkh, F_vrkl, F_vrkm = shearCapacity(beam.fastenerDiameter, beam.thickness, beam.timberGrade, beam.fastenerGrade, 0, beam.chi)
        
            beam.F_vrd = F_vrd
            beam.F_vrd1 = F_vrd1
            beam.F_vrd2 = F_vrd2
            beam.F_vrk1 = F_vrk1
            beam.F_vrk2 = F_vrk2
            beam.F_vrkf = F_vrkf
            beam.F_vrkg = F_vrkg 
            beam.F_vrkh = F_vrkh
            beam.F_vrkl = F_vrkl
            beam.F_vrkm = F_vrkm


    def calcPossibleFastener(ClassList):

        for beam in ClassList:

            a1 = beam.distancesFinal[0][0]
            a2 = beam.distancesFinal[0][1]
            a3 = beam.distancesFinal[0][2]
            a4 = beam.distancesFinal[0][3]
            e1 = beam.distancesFinal[0][4]


            beam.fastenerCheck = 2
            additionalFastener = 0

            while beam.fastenerCheck > 0.8:

                    additionalFastener += 1

                    noTotalReq = roundToBase(abs(beam.axialForce) / (beam.F_vrd * (beam.sheetNo * 2)), 1) + additionalFastener
                    noPerpPos = int((beam.height - 2 * a4) / a2)

                    beam.noPerp = int(max(3, noTotalReq)) if noTotalReq < noPerpPos else int(noPerpPos)
                    beam.distancesFinal[0][3] = (beam.height - a2 * (beam.noPerp - 1)) / 2

                    beam.noAxial = int(max(roundToBase(noTotalReq / beam.noPerp, 1), 1)) 
                    beam.noAxialEffective = round(effectiveNumber(beam.noAxial, a1, beam.fastenerDiameter), 2)

                    beam.noTotal = int(beam.noPerp * beam.noAxial)
                    beam.noTotalEffective = round(beam.noAxialEffective * beam.noPerp, 2)

                    beam.F_vrdTotal = round(beam.F_vrd * beam.noTotalEffective * (beam.sheetNo * 2), 2)
                    beam.fastenerCheck = round(abs(beam.axialForce) / beam.F_vrdTotal, 2)

            beam.sheetLength = e1 + a1 * (beam.noAxial ) + a3 * 2


    def checkNoSheets(ClassList):

        for beam in ClassList:
            test = 0
            if beam.noAxial >= 4:
                test = 1
        
        if test == 1:
            for beam in ClassList:
                beam.sheetNo = 2

        else: 
            a = 2


    def calcChosenFastener(ClassList):

        for beam in ClassList:

            a1 = beam.distancesFinal[0][0]
            a2 = beam.distancesFinal[0][1]
            a3 = beam.distancesFinal[0][2]
            a4 = beam.distancesFinal[0][3]
            e1 = beam.distancesFinal[0][4]
        
            beam.noAxialEffective = round(effectiveNumber(beam.noAxial, a1, beam.fastenerDiameter), 2)
            beam.noTotal = int(beam.noPerp * beam.noAxial)
            beam.noTotalEffective = round(beam.noAxialEffective * beam.noPerp, 2)
            beam.sheetLength = e1 + a1 * (beam.noAxial) + a3 * 2
            beam.distancesFinal[0][3] = (beam.height - a2 * (beam.noPerp - 1)) / 2
            beam.F_vrdTotal = round(beam.F_vrd * beam.noTotalEffective * (beam.sheetNo * 2), 2)

            beam.fastenerCheck = round(abs(beam.axialForce) / beam.F_vrdTotal, 2)


    # calculate fastener coordinates
    def calcFastenerCoordinates(ClassList):

        for beam in ClassList:

            a1 = beam.distancesFinal[0][0]
            a2 = beam.distancesFinal[0][1]
            a3 = beam.distancesFinal[0][2]
            a4 = beam.distancesFinal[0][3]
            e1 = beam.distancesFinal[0][4]

            # combine x and y coordinates with all possible combinations
            gapX = ClassList[0].height / 2 * sin(radians(beam.beamAngle)) 
            gapY = ClassList[0].height / 2 - beam.height / 2
            xCoordsFastener = [(2 * a3 + a1 * i) + gapX for i in range(int(beam.noAxial))]
            yCoordsFastener = [(a4 + a2 * i) + gapY for i in range(int(beam.noPerp))]
            combined_lists = list(product(xCoordsFastener, yCoordsFastener))

            # rotated xy coordinates
            xCoordsFastener = [combined_lists[i][0] for i in range(len(combined_lists))]
            yCoordsFastener = [combined_lists[i][1] for i in range(len(combined_lists))]
            xCoordsFastener, yCoordsFastener = rotateAroundPoint(xCoordsFastener, yCoordsFastener, -beam.beamAngle, (0, ClassList[0].height / 2))
            
            #st.write(xCoordsFastener)

            beam.xCoordinates.append(xCoordsFastener)
            beam.yCoordinates.append(yCoordsFastener)



    # calculate total forces due axial, shear and moment
    def calcAxialMemberCheck(ClassList):

        for beam in ClassList:

            if beam.axialForce > 0:

                A_net, f_t0k, f_td, tensionForce, sigma_t0d, beft, eta = tensionMemberCheck(beam.width, beam.height, beam.noPerp, beam.fastenerDiameter, beam.axialForce, beam.timberGrade, beam.sheetNo, beam.chi, beam.sheetThickness)
                beam.tensionMemberCheck = eta
                beam.Anet_axial = A_net
                beam.ft0k = f_t0k
                beam.ft0d = f_td
                beam.tensionForce = tensionForce
                beam.beft = beft
                beam.sigmat0d = sigma_t0d
            
            else:

                A_net, f_c0k, f_cd, compressionForce, sigma_c0d, befc, eta = compressionMemberCheck(beam.width, beam.height, beam.noPerp, beam.fastenerDiameter, beam.axialForce, beam.timberGrade, beam.sheetNo, beam.chi, beam.sheetThickness)
                beam.compressionMemberCheck = eta
                beam.Anet_axial = A_net
                beam.fc0k = f_c0k
                beam.fc0d = f_cd
                beam.compressionForce = compressionForce
                beam.befc = befc
                beam.sigmac0d = sigma_c0d


    # calculate total forces due axial, shear and moment
    def calcshearBlockFailureCheckAxial(ClassList):

        for beam in ClassList:

            # Function to check shear block failure
            Lh, Lv, Ant, Anv, VeffRd, eta = blockFailureCheckAxial(beam.fastenerGrade, beam.noPerp, beam.noAxial, beam.fastenerDiameter, beam.sheetThickness, beam.distancesFinal, beam.axialForce, beam.sheetNo)
            beam.axialBlockFailureCheck = eta
            beam.Lh1 = Lh
            beam.Lv1 = Lv
            beam.Ant1 = Ant
            beam.Anv1 = Anv
            beam.Veff1Rd = VeffRd

    def automaticDesign(beamClassesList):

        # get material porperties
        Beams.getkmod(beamClassesList)

        # distances
        Beams.getRequiredDistances(beamClassesList)

        # calculate fastener properties
        Beams.calcFastenerProperties(beamClassesList)

        # calculate fastener capacity due axial force and shear force
        Beams.calcFastenerCapacity(beamClassesList)

        # possible fastener
        Beams.calcPossibleFastener(beamClassesList)

        #
        Beams.checkNoSheets(beamClassesList)

        # calculate fastener capacity due axial force and shear force
        Beams.calcFastenerCapacity(beamClassesList)

        # possible fastener
        Beams.calcPossibleFastener(beamClassesList)

        # calculate fastener coordinates
        Beams.calcFastenerCoordinates(beamClassesList)

        # check axial
        Beams.calcAxialMemberCheck(beamClassesList)

        # check axial
        Beams.calcshearBlockFailureCheckAxial(beamClassesList)


    def manualDesign(beamClassesList, a1, a2, a3, a4):

        # get material porperties
        Beams.getkmod(beamClassesList)

        # distances
        Beams.defineDistances(beamClassesList, a1, a2, a3, a4)

        # calculate fastener properties
        Beams.calcFastenerProperties(beamClassesList)

        # calculate fastener capacity due axial force and shear force
        Beams.calcFastenerCapacity(beamClassesList)

        # distances
        Beams.calcChosenFastener(beamClassesList)

        # calculate fastener coordinates
        Beams.calcFastenerCoordinates(beamClassesList)

        # check axial
        Beams.calcAxialMemberCheck(beamClassesList)

        # check axial
        Beams.calcshearBlockFailureCheckAxial(beamClassesList)
   
    def createDictionaries(beam):

        dictLoadingParameter = {"kmod": [beam.k_mod], 
                           "gamma": [beam.gamma], 
                           "chi": [beam.chi], 
                           "Beam": [beam.name]}

        # timber
        dictTimber = {"Grade": [beam.timberGrade], 
                    "Width": [beam.width], 
                    "Height": [beam.height], 
                    "Beam": [beam.name]}
        
        # loading
        dictLoading = {"Axial": [beam.axialForce], 
                    "Beam": [beam.name]}

        # distances timber
        dictDistancesTimber = {"Alpha": [0],
                    "a_1": [beam.distancesTimber[0][0]], 
                    "a_2": [beam.distancesTimber[0][1]], 
                    "a_3t": [beam.distancesTimber[0][2]], 
                    "a_3c": [beam.distancesTimber[0][3]], 
                    "a_4t": [beam.distancesTimber[0][4]],
                    "a_4c": [beam.distancesTimber[0][5]]}

        # distances steel
        dictDistancesSteel = {"Diameter": [beam.fastenerDiameter], 
                    "e_1": [beam.distancesSteel[0][0]], 
                    "e_2": [beam.distancesSteel[0][1]], 
                    "p_1": [beam.distancesSteel[0][2]], 
                    "p_2": [beam.distancesSteel[0][3]]}

        # distances selected
        dictDistancesSelected = {"Alpha": [0],
                    "a_1": [beam.distancesFinal[0][0]], 
                    "a_2": [beam.distancesFinal[0][1]], 
                    "a_3": [beam.distancesFinal[0][2]],  
                    "a_4": [beam.distancesFinal[0][3]],  
                    "e_1": [beam.distancesFinal[0][4]]}

        # number of fastener
        dictFastenerNumber = {"No Perp": [beam.noPerp], 
                    "No Axial": [beam.noAxial], 
                    "No Axial Eff": [beam.noAxialEffective], 
                    "No Total": [beam.noTotal],
                    "No Eff": [beam.noTotalEffective],
                    "Beam": [beam.name]}

        # fastener
        dictFastener = { 
                    "fub": [beam.f_ub], 
                    "MyRk": [beam.M_yrk],
                    "fh0k": [beam.f_h0k],
                    "fhαk": [beam.f_halphak]}
        #F_vrkList

        # fastener Capacity
        dictFastenerCapacity = {"Angle": [0], 
                    "FvRk_f": [beam.F_vrkf],
                    "FvRk_g": [beam.F_vrkg],
                    "FvRk_h": [beam.F_vrkh],
                    "FvRk": [beam.F_vrk1],
                    "FvRd": [beam.F_vrd1],}

        # fastener Check
        dictFastenerCheck= {"Beam": [beam.name], 
                    "No Perp": [beam.noPerp], 
                    "No Axial": [beam.noAxial],  
                    "No Eff": [beam.noTotalEffective],
                    "FvRd":  [beam.F_vrdTotal], 
                    "eta": [beam.fastenerCheck]} 
        
        return dictLoadingParameter, dictTimber, dictLoading, dictDistancesTimber, dictDistancesSteel, dictDistancesSelected, dictFastenerNumber, dictFastener, dictFastenerCapacity, dictFastenerCheck

        