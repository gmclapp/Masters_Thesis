import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import z kJ/(kgK)
    sv_col = 7 # Entropy of saturated vapor kJ/(kgK)
        
    x1,y1,x2,y2 = mf.vlookup(working_fluid_db,
                             boil_pres, press_col, hv_col)
    
    h1 = mf.interpolate(x1,y1,x2,y2,boil_pres)
    
    x1,y1,x2,y2 = mf.vlookup(working_fluid_db,
                             boil_pres, press_col, sv_col)
    
    s1 = mf.interpolate(x1,y1,x2,y2,boil_pres)
    s2 = s1 # This is the adiabatic volumetric assumption in the turbine

    x1,y1,x2,y2 = mf.vlookup(working_fluid_db,
                             cond_pres, press_col, hl_col)
    
    h3 = mf.interpolate(x1,y1,x2,y2,cond_pres)
    
    x1,y1,x2,y2 = mf.vlookup(working_fluid_db,
                             cond_pres, press_col, sl_col)
    
    s3 = mf.interpolate(x1,y1,x2,y2,cond_pres)

    # get h3 enthalpy of a saturated liquid at condenser pressure
    # get s3 entropy of a saturated vapor at condenser pressure

    # determine if the working fluid is wet, dry, or adiabatic.

    x1,y1,x2,y2 = mf.vlookup(working_fluid_db,
                                   cond_pres, press_col, sl_col)

    s2f = mf.interpolate(x1,y1,x2,y2,cond_pres)
    x1,y1,x2,y2 = mf.vlookup(working_fluid_db,
                                   cond_pres, press_col, sv_col)

    s2g = mf.interpolate(x1,y1,x2,y2,cond_pres)

    try:
        quality = (s2 - s2f)/(s2g - s2f)
    except ZeroDivisionError:
        quality = 0
    
    h2f = h3

    
    # h2g = enthalpy at state 2 for a saturated liquid
    x1,y1,x2,y2 = mf.vlookup(working_fluid_db, cond_pres, press_col, hv_col)
    h2g = mf.interpolate(x1,y1,x2,y2, cond_pres)
    h2fg = h2g-h2f
    h2s = h2f + quality* h2fg
    h2 = h1 - eff_t*(h1 - h2s)

    x1,y1,x2,y2 = mf.vlookup(working_fluid_db, boil_pres, press_col, v_col)
    specific_vol_3 = mf.interpolate(x1,y1,x2,y2, boil_pres)
    h4 = h3 + (specific_vol_3*(boil_pres-cond_pres))/eff_p

    W_m = h1-h2-h4+h3 # kilowatts of power per kg/s of mass flow rate
    Qin_m = h1-h4 # kilowatts of heat trasfer in per kg/s of mass flow rate
    Qout_m = h2-h3 # kilowatts of heat transfer out per kg/s of mass flow rate
    efficiency = ((h1-h2) - (h4-h3))/(h1-h4)
    
##    print("Quality: {:4.2f}\nPower: {:4.2f}kW/(kg/s)\nEfficiency: {:4.2f}" \
##          .format(quality, W_m, efficiency))
##    print("Heat in: {:4.2f}kW/(kg/s)\nHeat out: {:4.2f} kW/(kg/s)"\
##          .format(Qin_m,Qout_m))

    x1, y1, x2, y2 = mf.vlookup(working_fluid_db,
                               cond_pres, press_col, temp_col)
    cond_temp = mf.interpolate(x1,y1,x2,y2,cond_pres)
    x1,y1,x2,y2 = mf.vlookup(working_fluid_db,
                            boil_pres, press_col, temp_col)
    boil_temp = mf.interpolate(x1,y1,x2,y2,boil_pres)
##    print("Condenser temperature: {:4.2f} deg Celsius\nBoiler temperature: {:4.2f} deg Celsius" \
##          .format(cond_temp,boil_temp))
    return(W_m,efficiency,boil_temp,cond_temp,Qin_m,Qout_m)

#------Main------#
if __name__ == '__main__':
    '''Manual entry begins here.'''
    condenser_pressure = si.get_real_number("Enter condenser pressure (MPa).\n>>>",lower = 0)
    boiler_pressure = si.get_real_number("Enter boiler pressure (MPa).\n>>>", lower = condenser_pressure)
    turbine_efficiency = si.get_real_number("Enter the turbine efficiency (0-1).\n>>>",
                                            upper=1.0,lower=0)
    pump_efficiency = si.get_real_number("Enter the pump efficiency (0-1).\n>>>",
                                         upper=1.0, lower=0)
    max_heat = si.get_real_number("Enter maximum heat source temperature (C).\n>>>", lower = -273)

    # Run cycle model
    boil_temp = float("Inf")
    while boil_temp > max_heat:
        (Wm,efficiency,boil_temp,cond_temp,Qin_m,Qout_m) = ORC_model(condenser_pressure,boiler_pressure,turbine_efficiency,pump_efficiency)
        boiler_pressure -= 0.01
        
    print("Boiler pressure: {}".format(boiler_pressure))
    
    # Determine boiler heat exchanger size
    lmtd = LMTD(T_hot_in, T_hot_out, T_cold_in, T_cold_out)

    time.sleep(30)
else:
    pass
