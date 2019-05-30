import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import misc_functions as mf
import sanitize_inputs as si
import time

def LMTD(Tin, Tout, tin, tout):
    '''This function determines the log mean temperature difference of two
    working fluids where the temperature at the inlet and outlet of both
    fluids is known. This function is valid for a counter flow heat
    exchanger.'''

    LMTD = ((Tin-tout) - (tin-Tout)) / math.log((Tin-tout)/(tin-Tout))
    return(LMTD)

def boiler_model():
    pass
def condenser_model():
    pass
def turbine_model():
    pass
def pump_model():
    pass
def ORC_model(cond_pres, boil_pres, eff_t, eff_p):
    '''This function takes a working pressure for a condenser and boiler, an
    efficiency for a pump and turbine, and outputs the work per unit mass flow
    and thermal efficiency for a generic ORC, as well as the working temperature
    and enthalpy at each of the four fixed states which can then be used in the
    models for the individual major components.'''

    R245fa_db = '\\R245fa Saturated properties temperature table.csv'
    db_path = r'C:\Users\Glenn Clapp\Documents\GitHub\Masters_Thesis\GHSP study\Additional references'

    temp_col = 0 # Degrees Celsius
    press_col = 1 # MPa
    v_col = 3 # Specific volume of vapor m3/kg
    hl_col = 4 # Enthalpy of saturated liquid kJ/kg
    hv_col = 5 # Enthalpy of saturated vapor kJ/kg
    sl_col = 6 # Entropy of saturated liquid kJ/(kgK)
    sv_col = 7 # Entropy of saturated vapor kJ/(kgK)
        
    x1,y1,x2,y2 = mf.vlookup(db_path+R245fa_db,
                             boil_pres, press_col, hv_col)
    
    h1 = mf.interpolate(x1,y1,x2,y2,boil_pres)
    
    x1,y1,x2,y2 = mf.vlookup(db_path+R245fa_db,
                             boil_pres, press_col, sv_col)
    
    s1 = mf.interpolate(x1,y1,x2,y2,boil_pres)
    s2 = s1 # This is the adiabatic volumetric assumption in the turbine

    x1,y1,x2,y2 = mf.vlookup(db_path+R245fa_db,
                             cond_pres, press_col, hl_col)
    
    h3 = mf.interpolate(x1,y1,x2,y2,cond_pres)
    
    x1,y1,x2,y2 = mf.vlookup(db_path+R245fa_db,
                             cond_pres, press_col, sl_col)
    
    s3 = mf.interpolate(x1,y1,x2,y2,cond_pres)

    # get h3 enthalpy of a saturated liquid at condenser pressure
    # get s3 entropy of a saturated vapor at condenser pressure

    # determine if the working fluid is wet, dry, or adiabatic.

    x1,y1,x2,y2 = mf.vlookup(db_path+R245fa_db,
                                   cond_pres, press_col, sl_col)

    s2f = mf.interpolate(x1,y1,x2,y2,cond_pres)
    x1,y1,x2,y2 = mf.vlookup(db_path+R245fa_db,
                                   cond_pres, press_col, sv_col)

    s2g = mf.interpolate(x1,y1,x2,y2,cond_pres)

    try:
        quality = (s2 - s2f)/(s2g - s2f)
    except ZeroDivisionError:
        quality = 0
    
    h2f = h3

    
    # h2g = enthalpy at state 2 for a saturated liquid
    x1,y1,x2,y2 = mf.vlookup(db_path+R245fa_db, cond_pres, press_col, hv_col)
    h2g = mf.interpolate(x1,y1,x2,y2, cond_pres)
    h2fg = h2g-h2f
    h2s = h2f + quality* h2fg
    h2 = h1 - eff_t*(h1 - h2s)

    x1,y1,x2,y2 = mf.vlookup(db_path+R245fa_db, boil_pres, press_col, v_col)
    specific_vol_3 = mf.interpolate(x1,y1,x2,y2, boil_pres)
    h4 = h3 + (specific_vol_3*(boil_pres-cond_pres))/eff_p

    W_m = h1-h2-h4+h3 # kilowatts of power per kg/s of mass flow rate
    efficiency = ((h1-h2) - (h4-h3))/(h1-h4)
    
    print("Quality: {:4.2f}\nPower: {:4.2f}kW/(kg/s)\nEfficiency: {:4.2f}" \
          .format(quality, W_m, efficiency))

    x1, y1, x2, y2 = mf.vlookup(db_path+R245fa_db,
                               cond_pres, press_col, temp_col)
    cond_temp = mf.interpolate(x1,y1,x2,y2,cond_pres)
    x1,y1,x2,y2 = mf.vlookup(db_path+R245fa_db,
                            boil_pres, press_col, temp_col)
    boil_temp = mf.interpolate(x1,y1,x2,y2,boil_pres)
    print("Condenser temperature: {:4.2f} deg Celsius\nBoiler temperature: {:4.2f} deg Celsius" \
          .format(cond_temp,boil_temp))
    return(W_m,efficiency,boil_temp,cond_temp)

#------Main------#
if __name__ == '__main__':
    '''Manual entry begins here.'''
    condenser_pressure = si.get_real_number("Enter condenser pressure (MPa).\n>>>")
    boiler_pressure = si.get_real_number("Enter boiler pressure (MPa).\n>>>")
    turbine_efficiency = si.get_real_number("Enter the turbine efficiency (0-1).\n>>>",
                                            upper=1.0,lower=0)
    pump_efficiency = si.get_real_number("Enter the pump efficiency (0-1).\n>>>",
                                         upper=1.0, lower=0)
    max_heat = si.get_real_number("Enter maximum heat source temperature (K).\n>>>")
    (Wm,efficiency,boil_temp,cond_temp) = ORC_model(condenser_pressure,
              boiler_pressure,
              turbine_efficiency,
              pump_efficiency)

    time.sleep(30)
else:
    pass
