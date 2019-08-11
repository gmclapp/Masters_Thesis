import csv
import math
import sanitize_inputs as si
import time
import os
import CoolProp.CoolProp as CP

def ORC_model(cond_pres, boil_pres, eff_t, eff_p,working_fluid_db):
    '''This function takes a working pressure for a condenser and boiler, an
    efficiency for a pump and turbine, and outputs the work per unit mass flow
    and thermal efficiency for a generic ORC, as well as the working temperature
    and enthalpy at each of the four fixed states which can then be used in the
    models for the individual major components.'''

    fluid = 'R245fa'

    h1 = CP.PropsSI('H', 'P', boil_pres*1000000, 'Q', 1, 'R245fa')/1000
    s1 = CP.PropsSI('S','P',boil_pres*1000000, 'Q', 1, fluid)/1000
    
    
    h3 = CP.PropsSI('H', 'P', cond_pres*1000000, 'Q', 0, fluid)/1000
    s3 = CP.PropsSI('S','P',cond_pres*1000000, 'Q', 0, fluid)/1000

    s2 = s1
    s2f = CP.PropsSI('S','P', cond_pres*1000000,'Q',0,fluid)/1000
    s2g = CP.PropsSI('S','P', cond_pres*1000000,'Q',1,fluid)/1000

    
    try:
        quality = (s2 - s2f)/(s2g - s2f)
    except ZeroDivisionError:
        quality = 0
    if quality > 1:
        print("Turbine outlet is superheated vapor! x = {:4.4f}".format(quality))
        h2s = CP.PropsSI('H','S',s2*1000,'P', cond_pres*1000000, fluid)/1000

    elif 0 <= x <= 1:
        h2f = h3

        h2g = CP.PropsSI('H','P', cond_pres*1000000, 'Q',1,fluid)/1000

        
        h2fg = h2g-h2f
        h2s = h2f + quality* h2fg

    h2 = h1 - eff_t*(h1 - h2s)

    specific_vol_3 = 1/CP.PropsSI('D','P',boil_pres*1000000,'Q',1,fluid)
 
    h4 = h3 + (specific_vol_3*(boil_pres-cond_pres))/eff_p

    W_m = h1-h2-h4+h3 # kilowatts of power per kg/s of mass flow rate
    Qin_m = h1-h4 # kilowatts of heat trasfer in per kg/s of mass flow rate
    Qout_m = h2-h3 # kilowatts of heat transfer out per kg/s of mass flow rate
    efficiency = ((h1-h2) - (h4-h3))/(h1-h4)

    cond_temp = CP.PropsSI('T','P',cond_pres*1000000,'Q',1,fluid)-273
    boil_temp = CP.PropsSI('T','P',boil_pres*1000000,'Q',1,fluid)-273

    return(W_m,efficiency,boil_temp,cond_temp,Qin_m,Qout_m)

#------Main------#
if __name__ == '__main__':
    R245fa_db = '\\R245fa Saturated properties temperature table.csv'
    os.chdir("..")# Navigate up a directory
    db_path=os.path.abspath(os.curdir)+r"\GHSP study\Additional references"+R245fa_db
    # Navigate to the directory containing the working fluid database.
    
    '''Manual entry begins here.'''
    condenser_pressure = si.get_real_number("Enter condenser pressure (MPa).\n>>>",lower = 0)
    boiler_pressure = si.get_real_number("Enter boiler pressure (MPa).\n>>>", lower = condenser_pressure)
    turbine_efficiency = si.get_real_number("Enter the turbine efficiency (0-1).\n>>>",
                                            upper=1.0,lower=0)
    pump_efficiency = si.get_real_number("Enter the pump efficiency (0-1).\n>>>",
                                         upper=1.0, lower=0)
    max_heat = si.get_real_number("Enter maximum heat source temperature (C).\n>>>", lower = -273)

    (Wm,efficiency,boil_temp,cond_temp,Qin_m,Qout_m) = ORC_model(condenser_pressure,boiler_pressure,turbine_efficiency,pump_efficiency,db_path)
    print("Power: {}\nEfficiency: {}\nCondenser temperature: {}\nBoiler temperature: {}"\
          .format(Wm,efficiency,cond_temp,boil_temp))


    time.sleep(30)
else:
    pass
