from math import * # Import math module for mathematical functions
from itertools import product
from functions_plotly import *
from functions_distances import *
from functions_material_properties import *
from functions_force_distribution import *
from functions_fastener_capacity import *
from functions_member_checks import *
from classes import *

def report(beam):

    # report
    text = "Beam"
    header = f'<p style="font-family:Arial; color:rgb(0,0,0); font-size: 17px; font-weight: bold; ">Report for Beam {text}</p>'
    st.markdown(header, unsafe_allow_html=True)

    # create dictionaries
    dictLoadingParameter, dictTimber, dictLoading, dictDistancesTimber, dictDistancesSteel, dictDistancesSelected, dictFastenerNumber, dictFastener, dictFastenerCapacity, dictFastenerCheck = Beams.createDictionaries(beam)

    # tables
    dfFastener = pd.DataFrame(dictFastener).set_index('fub')
    dfFastenerNumber = pd.DataFrame(dictFastenerNumber).set_index('Beam')
    dfDistancesTimber = pd.DataFrame(dictDistancesTimber).set_index('Alpha')
    dfDistancesSteel = pd.DataFrame(dictDistancesSteel).set_index('Diameter')
    dfDistancesSelected = pd.DataFrame(dictDistancesSelected).set_index('Alpha')
    dfLoading = pd.DataFrame(dictLoading).set_index('Beam')
    dfTimber = pd.DataFrame(dictTimber).set_index('Beam')
    dfLoadingPara = pd.DataFrame(dictLoadingParameter).set_index('Beam')
    dfFastenerCapacity = pd.DataFrame(dictFastenerCapacity).set_index('Angle')
    dfFastenerCheck = pd.DataFrame(dictFastenerCheck).set_index('Beam')

    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">System</p>'
    st.markdown(header, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Timber Parameters")
        st.write(dfTimber)

    with col2:
        st.write("Loading")
        st.write(dfLoading)

    st.write("Load Parameters")
    st.write(dfLoadingPara)
    
    st.write('Resistance reduction factor')
    st.latex(r''' \chi = \frac{k_{mod}}{\gamma}= ''' + str(round(beam.chi, 2)))

    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 25px; font-weight: bold; ">Fastener</p>'
    st.markdown(header, unsafe_allow_html=True)

    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">Spacings</p>'
    st.markdown(header, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Timber")
        st.caption('DIN EN 1995-1-1 Ch. 8.6 Tab.8.5')
        st.write(dfDistancesTimber)

    with col2:
        st.write("Steel")
        st.caption('DIN EN 1993-1-1 ..')
        st.write(dfDistancesSteel)

    st.write("Selected")
    st.write(dfDistancesSelected)

    # drawDistances(beam)

    col1, col2, col3 = st.columns(3)
    with col1:
        header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">Properties</p>'
        st.markdown(header, unsafe_allow_html=True)
        st.caption('DIN EN 1995-1-1 Ch. 8.5.1.1')

        st.write("Summary")
        st.write(dfFastener)

        st.write('Characteristic value for the yield moment')
        st.latex(r''' M_{yRk} = f_{ub} * d^{2.6}= ''' + str(beam.M_yrk)+ "Nmm")
        
        st.write('Characteristic tensile strengtht parallel to the grain')
        st.latex(r''' f_{h0k} = 0.082 * (1 - 0.01 * d) * \rho_{k} = ''' + str(beam.f_h0k) + r''' \frac{N}{mm^2}''')
        
 
    st.write("")
    st.write("")
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">Capacity</p>'
    st.markdown(header, unsafe_allow_html=True) 
    st.caption('DIN EN 1995-1-1 Ch. 8.2.3-8.11 Eq. f-h')

    st.write("Summary")
    st.write(dfFastenerCapacity)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 15px; font-weight: bold; ">Single sheet</p>'
        st.markdown(header, unsafe_allow_html=True)
        st.caption('Equation 8.11f')
        st.latex(r''' F_{vk1} = f_{hk}*t_{1}*d =  ''' 
                + str(beam.F_vrkf) + ' kN')
        st.caption('Equation 8.11g')
        st.latex(r''' F_{vk2} = f_{hk}*t_{2}*d * \left( \sqrt{2+ r( \frac{4*M_{yRk}}{f_{hk}*d*t_{1}^2}} ) \right) = ''' 
                + str(beam.F_vrkg) + ' kN')
        st.caption('Equation 8.11h')
        st.latex(r''' F_{vk3} = 2.3 * \sqrt{2*M_{yRk}*f_{hk}*d} = ''' 
                + str(beam.F_vrkh) + ' kN')
        st.caption('')
        st.caption('')
        st.caption('')
        st.caption('')
        st.caption('')
        st.caption('')
        st.latex(r'''  F_{vRk1} = min( ''' + rf'''{beam.F_vrkf}, ''' + rf'''{beam.F_vrkg}, ''' + rf'''{beam.F_vrkh}) = ''' + str(beam.F_vrk1) + ' kN')
        st.latex(r''' F_{vRd1} = F_{vRk} * \frac{k_{mod}}{\gamma} = ''' + str(beam.F_vrd1) + ' kN')

    if beam.sheetNo == 2:
        with col3:
            header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 15px; font-weight: bold; ">Double sheet</p>'
            st.markdown(header, unsafe_allow_html=True)
            st.caption('Equation 8.11f')
            st.latex(r''' F_{vk1} = f_{hk}*t_{1}*d =  ''' 
                    + str(beam.F_vrkf) + ' kN')
            st.caption('Equation 8.11h')
            st.latex(r''' F_{vk3} = 2.3 * \sqrt{2*M_{yRk}*f_{hk}*d} = ''' 
                    + str(beam.F_vrkh) + ' kN')
            st.caption('')
            st.caption('')
            st.caption('Equation 8.11l')
            st.latex(r''' F_{vk1} = 0.5 * f_{hk}*t_{2}*d =  ''' 
                    + str(beam.F_vrkl) + ' kN')
            st.caption('Equation 8.11m')
            st.latex(r''' F_{vk3} = 2.3 * \sqrt{2*M_{yRk}*f_{hk}*d} = ''' 
                    + str(beam.F_vrkm) + ' kN')
            st.latex(r'''  F_{vRk2} = min( ''' + rf'''{beam.F_vrkf}, ''' + rf'''{beam.F_vrkh}, ''' + rf'''{beam.F_vrkl}, ''' + rf'''{beam.F_vrkm}) = ''' + str(beam.F_vrk2) + ' kN')
            st.latex(r''' F_{vRd2} = F_{vRk} * \frac{k_{mod}}{\gamma} = ''' + str(beam.F_vrd2) + ' kN')



    st.write("")
    st.write("")
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 25px; font-weight: bold; ">Checks</p>'
    st.markdown(header, unsafe_allow_html=True)

    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">1. Fastener Check</p>'
    st.markdown(header, unsafe_allow_html=True)
    st.write("Summary")
    st.write(dfFastenerCheck)

    st.write('Number of fastener')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.latex(r''' n_{axial} = ''' + str(beam.noAxial))
    with col2:
        st.latex(r''' n_{perp} = ''' + str(beam.noPerp))
    with col3:
        st.latex(r''' n_{total} = ''' + str(beam.noTotal))

    st.write('Effective number of fastener')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.latex(r''' n_{eff} = ''' + str(beam.noAxialEffective))
    with col2:
        st.latex(r''' n_{total.eff} = ''' + str(beam.noTotalEffective))

    st.write('Design loading')
    st.latex(r''' F_{xEd} = ''' + str(abs(beam.axialForce)) + ' kN')

    st.write('Resistance')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.latex(r''' F_{vRd} = ''' + str(beam.F_vrd) + ' kN')
    with col2:
        st.latex(r''' F_{vRd.total} = ''' + str(beam.F_vrdTotal) + ' kN')
    
    st.write('Utilization')
    st.latex(r''' \eta = \frac{F_{xEd}}{F_{vRd.total}} =''' + str(beam.fastenerCheck))



    # AXIAL STRESS CHECK
    if beam.axialForce > 0:

        st.write("")
        header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">2. Member Tension Check</p>'
        st.markdown(header, unsafe_allow_html=True)
        st.caption('DIN EN 1995-1-1 Abs. 6.1.7')

        st.write('Design tension load')
        st.latex(r''' N_{td} = ''' + str(beam.tensionForce) + ' kN')

        st.write('Resistance')
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write('Characteristic tensile strength')
            st.latex(r''' f_{t0k} = ''' + str(beam.ft0k) + r''' \frac{N}{mm^2}''')
        with col2:
            st.write('Design tensile strength')
            st.latex(r''' f_{t0d} = f_{t0k} * \chi * 0.4 = ''' + str(beam.ft0d) + r''' \frac{N}{mm^2}''')

        st.write('Net area of timber')
        st.latex(r''' b_{ef} = \frac{B}{n_{sheet} + 1} - \frac{t_{sheet}}{2} =''' + str(beam.beft) + r''' cm''')
        st.latex(r''' A_{net} = H * b_{ef} - n_{perp} * d * b_{ef} =''' + str(round(beam.Anet_axial * 0.01, 2)) + r''' cm^2''')

        st.write('Design tensile stress')
        st.latex(r''' \sigma_{t0d} = \frac{ N_{td} }{A_{net}} = ''' + str(beam.sigmat0d) + r''' \frac{N}{mm^2}''')

        st.write('Utilization')
        st.caption("DIN EN 1995-1-1 Eq. 6.1")
        st.latex(r''' \eta = \frac{\sigma_{t0d}}{f_{t0d} } =''' + str(beam.tensionMemberCheck))

    else:

        st.write("")
        header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">2. Member Compression Check</p>'
        st.markdown(header, unsafe_allow_html=True)
        st.caption('DIN EN 1995-1-1 Abs. 6.1.7')

        st.write('Design compression load')
        st.latex(r''' N_{cd} = ''' + str(beam.compressionForce) + ' kN')

        st.write('Resistance')
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.write('Characteristic compressive strength')
            st.latex(r''' f_{c0k} = ''' + str(beam.fc0k) + r''' \frac{N}{mm^2}''')
        with col2:
            st.write('Design compressive strength')
            st.latex(r''' f_{c0d} = f_{c0k} * \chi = ''' + str(beam.fc0d) + r''' \frac{N}{mm^2}''')

        st.write('Net area of timber')
        st.latex(r''' b_{ef} = \frac{B}{n_{sheet} + 1} - \frac{t_{sheet}}{2} =''' + str(beam.befc) + r''' cm''')
        st.latex(r''' A_{net} = H * b_{ef} =''' + str(round(beam.Anet_axial * 0.01, 2)) + r''' cm^2''')

        st.write('Design compressive stress')
        st.latex(r''' \sigma_{c0d} = \frac{ N_{cd} }{A_{net}} = ''' + str(beam.sigmac0d) + r''' \frac{N}{mm^2}''')

        st.write('Utilization')
        st.caption("DIN EN 1995-1-1 Eq. 6.2")
        st.latex(r''' \eta = \frac{\sigma_{c0d}}{f_{c0d} } =''' + str(beam.compressionMemberCheck))


    st.write("")
  
    header = '<p style="font-family:Arial; color:rgb(0,0,0); font-size: 20px; font-weight: bold; ">3. Axial Block Failure Check</p>'
    st.markdown(header, unsafe_allow_html=True)
    st.caption('DIN EN 1993-1-1 Abs. 6.1.7')

    st.write('Fastener')
    f_u, f_y = getTensileStrength(beam.fastenerGrade)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.latex(r''' f_{u} = ''' + str(f_u) + r''' \frac{N}{mm^2}''')
    with col2:
        st.latex(r''' f_{y} = ''' + str(f_y) + r''' \frac{N}{mm^2}''')

    st.latex(r''' d_{0} = d + 0.6 mm = ''' + str(beam.fastenerDiameter + 0.6) + ' mm')

    st.write('Effective areas')

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.latex(r''' L_{h} = a_{2} * (n_{perp} - 1) = ''' + str(beam.Lh1) + r''' mm''')
    with col3:
        st.latex(r''' L_{v} = a_{1} * (n_{axial} - 1) + e_{1} = ''' + str(beam.Lv1) + r''' mm''')
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.latex(r''' A_{nt} = (L_{h} - (n_{axial} - 1) * d_{0}) * t = ''' + str(beam.Ant1) + r''' cm^2''')
    with col3:
        st.latex(r''' A_{nv} = 2 * (L_{v} - (n_{perp} - 0.5) * d_{0}) * t = ''' + str(beam.Anv1) + r''' cm^2''')
    
    st.write('Resistance')
    st.latex(r''' V_{eff.Rd} = \frac{f_{u} * A_{nt}}{1.25} + \frac{f_{y} * A_{nv}}{ \sqrt{3} + 1 } = ''' + str(beam.Veff1Rd) + r'''kN''')
    
    st.write('Design axial load')
    st.latex(r''' N_{ed} = ''' + str(abs(beam.axialForce)) + ' kN')
    
    st.write('Utilization')
    st.latex(r''' \eta = \frac{ N_{ed} }{ V_{eff.Rd}} = ''' + str(beam.axialBlockFailureCheck))
