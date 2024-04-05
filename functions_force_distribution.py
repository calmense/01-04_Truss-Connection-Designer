# ============= FUNCTION ==========================================
# _____________ Bolt group force distribution ______________________

from math import *  # Import all functions and constants from the math module
import plotly.graph_objects as go  # Import plotly for creating interactive plots
import streamlit as st  # Import streamlit for creating web applications

class Fastener:
    def __init__(self, name, x, y, area, rx, ry, rxy, alpha, ShearX, ShearY, ShearXY):
        # Constructor to initialize Fastener object
        self.name = name  # Name of the fastener
        self.x = x  # x-coordinate of the fastener
        self.y = int(y)  # y-coordinate of the fastener
        self.area = area  # Area of the fastener
        self.rx = rx  # x-distance to centroid
        self.ry = ry  # y-distance to centroid
        self.rxy = rxy  # xy-distance to centroid
        self.alpha = alpha  # Angle of resultant shear force
        self.ShearX = ShearX  # Shear force along x-direction
        self.ShearY = ShearY  # Shear force along y-direction
        self.ShearXY = ShearXY  # Shear force along xy-direction

    @staticmethod
    def calc_centroid(xCoordinates, yCoordinates, diameter):
        # Method to calculate centroid of the bolt pattern
        numberFastener = len(xCoordinates)  # Number of fasteners
        area = round(pi*diameter**2 / 4,1)  # Area of each fastener
        totalArea = int(area * numberFastener)  # Total area of all fasteners
        
        # Initialize fastener list and product lists
        fastenerList = []
        productxList = []
        productyList = []

        # Create Fastener objects and calculate product of x and y coordinates with area
        for i in range(numberFastener):
            point = Fastener(f"F{i}", xCoordinates[i], yCoordinates[i], area, None, None, None, None, None, None, None)
            fastenerList.append(point)
            productxi = point.x * point.area
            productyi = point.y * point.area
            productxList.append(productxi)
            productyList.append(productyi)

        # Calculate centroid coordinates
        centroid_cx = round(sum(productxList) / totalArea,2)
        centroid_cy = round(sum(productyList) / totalArea,2)

        return fastenerList, centroid_cx, centroid_cy, area
    
    @staticmethod
    def calc_polar_moment_of_intertia(fastenerList, centroid_cx, centroid_cy):
        # Method to calculate polar moment of inertia of the bolt pattern
        IcxList = []
        IcyList = []
        rxyList = []

        # Iterate through fasteners to calculate bolt pattern moments of inertia
        for i in range(len(fastenerList)):
            rxi = round(fastenerList[i].x - centroid_cx,1)  # x-distance to centroid
            ryi = round(fastenerList[i].y - centroid_cy,1)  # y-distance to centroid
            rxyi = round(sqrt(rxi**2 + ryi**2),1)  # xy-distance to centroid
            Icxi = rxi**2 * fastenerList[i].area  # centroidal moment of inertia about the X-axis
            Icyi = ryi**2 * fastenerList[i].area  # centroidal moment of inertia about the Y-axis
            
            # Update Fastener object attributes
            setattr(fastenerList[i], "rx", rxi)
            setattr(fastenerList[i], "ry", ryi)
            setattr(fastenerList[i], "rxy", rxyi)
            IcxList.append(Icxi)
            IcyList.append(Icyi)
            rxyList.append(rxyi**2)

        # Calculate polar moment of inertia
        Icx = int(sum(IcxList))  # centroidal moment of inertia about the X-axis
        Icy = int(sum(IcyList))  # centroidal moment of inertia about the Y-axis
        Icp = Icx + Icy  # polar moment of inertia

        return Icp
    
    @staticmethod
    def calc_shear_forces(fastenerList, Icp, Moment):
         
        shearXList = []
        shearYList = []
        shearXYList = []

        for i in range(len(fastenerList)):

            ShearXY = (Moment * fastenerList[i].rxy * fastenerList[i].area / Icp) * 1000
            ShearX = (-fastenerList[i].ry * Moment / Icp) * 1000
            ShearY = (fastenerList[i].rx * Moment / Icp) * 1000
        
            alpha = atan(ShearY/ShearX)

            setattr(fastenerList[i], "ShearX", round(ShearX,3))
            setattr(fastenerList[i], "ShearY", round(ShearY,3))
            setattr(fastenerList[i], "ShearXY", round(ShearXY, 3))
            setattr(fastenerList[i], "alpha", round(alpha * 180 / pi,1))

            shearXList.append(ShearX)
            shearYList.append(ShearY)
            shearXYList.append(ShearXY)
        
        totalShearX = sum(shearXList)
        totalShearY = sum(shearYList)
        totalShearXY = sqrt(totalShearX**2 + totalShearY**2)

        return shearXList, shearYList, shearXYList, totalShearX, totalShearY, totalShearXY, alpha
       
    @staticmethod
    def get_arrow_propotions(shearXList, shearYList, shearXYList):

        # Bolt force arrows
        maxShearX = max(shearXList)
        maxShearY = max(shearYList)
        maxShearXY = max(shearXYList)

        shearXProp = [shearXi / maxShearX for shearXi in shearXList]
        shearYProp = [shearYi / maxShearY for shearYi in shearYList]
        shearXYProp = [shearXYi / maxShearXY for shearXYi in shearXYList]

        arrowLength = 30
        arrowListx = [arrowLength * shearXProp[i] for i in range(len(shearXList))]
        arrowListy = [arrowLength * shearYProp[i] for i in range(len(shearXList))]

        return arrowListx, arrowListy
        
    @staticmethod
    def calc_shear_distribution(xCoordinates, yCoordinates, diameter, Moment):

        fastenerList, centroid_cx, centroid_cy, area = Fastener.calc_centroid(xCoordinates, yCoordinates, diameter)
        Icp = Fastener.calc_polar_moment_of_intertia(fastenerList, centroid_cx, centroid_cy)
        shearXList, shearYList, shearXYList, totalShearX, totalShearY, totalShearXY, alpha = Fastener.calc_shear_forces(fastenerList, Icp, Moment)
        arrowListx, arrowListy = Fastener.get_arrow_propotions(shearXList, shearYList, shearXYList)

        return centroid_cx, centroid_cy, Icp, shearXList, shearYList, shearXYList, arrowListx, arrowListy, alpha