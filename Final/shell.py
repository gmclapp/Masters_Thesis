import ORC_Model as orc
import heat_exchanger_model as heatex
import os
import numpy as np
import pandas as pd
import time
import sanitize_inputs as si

np.set_printoptions(precision=3)
# Sets the decimal precision when printing numpy arrays to 3. Note that further
# significant figures are preserved, just not printed.

def find_max_boiler(condenser_pressure, boiler_pressure, turbine_efficiency, pump_efficiency, max_source_temp, db_path):

    test_temp = 0
    b_temp = max_source_temp-0.1
    while test_temp < b_temp:
        (Wm,eff,b_temp,c_temp,Qin_m,Qout_m) = orc.ORC_model(condenser_pressure,
                                                            boiler_pressure,
                                                            turbine_efficiency,
                                                            pump_efficiency,
                                                            db_path)
        test_temp = heatex.feedwater_exit_temp(max_source_temp, 3.7682,Qin_m)
        
        print("T: {:4.2f} deg, P: {:4.2f} MPa".format(test_temp, boiler_pressure))
        boiler_pressure -= 0.01
    print("Power: {:4.2f}kW/(kg/s)\nEfficiency: {:4.2f}" .format(Wm, eff))
    print("Heat in: {:4.2f}kW/(kg/s)\nHeat out: {:4.2f} kW/(kg/s)".format(Qin_m,Qout_m))
    print("Condenser temperature: {:4.2f} deg Celsius\nBoiler temperature: {:4.2f} deg Celsius".format(c_temp,b_temp))
    print("Boiler pressure: {:4.2f} MPa".format(boiler_pressure))
    
def find_best(condenser_pressure, boiler_pressure, turbine_efficiency=0.9,
              pump_efficiency=0.9):
    '''Takes a condenser and boiler working pressure, isentropic efficiencies of
    the turbine and pump, and returns the best combination to maximize power per
    unit mass flow rate and thermal efficiency.'''
    
    max_power = 0
    power_b_pressure = None # boiler working pressure at max power
    power_c_pressure = None # condenser working pressure at max power
    
    max_efficiency = 0
    efficiency_b_pressure = None # boiler working pressure at max efficiency
    efficiency_c_pressure = None # condenser working pressure at max efficiency
    
    for c in condenser_pressure:
        for b in boiler_pressure:
            (Wm,eff,b_temp,c_temp,Qin_m,Qout_m) = orc.ORC_model(c,
                                                                b,
                                                                turbine_efficiency,
                                                                pump_efficiency,
                                                                db_path)
            if Wm > max_power:
                max_power = Wm
                power_b_pressure = b
                power_c_pressure = c

            if eff > max_efficiency:
                max_efficiency = eff
                efficiency_b_pressure = b
                efficiency_c_pressure = c
    return(max_power,
           power_b_pressure,
           power_c_pressure,
           max_efficiency,
           efficiency_b_pressure,
           efficiency_c_pressure)
                    
    
R245fa_db = '\\R245fa Saturated properties temperature table.csv'

db_upper_pressure_limit = 3.651
db_lower_pressure_limit = 0.00127

os.chdir("..")# Navigate up a directory
db_path=os.path.abspath(os.curdir)+r"\GHSP study\Additional references"+R245fa_db
# Navigate to the directory containing the working fluid database.

p_boiler_max = si.get_real_number("Enter the boiler working pressure upper limit (MPa):\n",upper=db_upper_pressure_limit,lower=db_lower_pressure_limit)
p_boiler_min = si.get_real_number("Enter the boiler working pressure lower limit (MPa):\n",upper=p_boiler_max,lower=db_lower_pressure_limit)

p_condenser_max = si.get_real_number("Enter the condenser working pressure upper limit (MPa):\n",upper=p_boiler_min,lower=db_lower_pressure_limit)
p_condenser_min = si.get_real_number("Enter the condenser working pressure upper limit (MPa):\n",upper=p_condenser_max,lower=db_lower_pressure_limit)
turbine_efficiency = si.get_real_number("Enter isentropic turbine efficiency (0-1):\n",upper=1,lower=0)# Study value = 0.787
pump_efficiency = si.get_real_number("Enter isentropic pump efficiency (0-1):\n",upper=1,lower=0)# Study value = 0.9

max_source_temp = si.get_real_number("Enter the maximum heat source temperature:\n")

# Creates a numpy array with 25 data points between p_condenser_min and p_condenser_max.
condenser_pressure_range = np.linspace(p_condenser_min, p_condenser_max, 25)
##boiler_pressure_range = np.linspace(p_boiler_min, p_boiler_max, 25)

##condenser_pressure = 0.13
##boiler_pressure = 1.26
##turbine_efficiency = 0.787
##pump_efficiency = 0.9
##max_source_temp = 97.5

find_max_boiler(p_condenser_min, p_boiler_max, turbine_efficiency, pump_efficiency, max_source_temp, db_path)

user = None
while(1):
    user = input()
    if user == 'q':
        break
    else:
        pass

##power,b_power,c_power,eff,b_eff,c_eff =find_best(condenser_pressure_range,
##                                                 boiler_pressure_range,
##                                                 turbine_efficiency,
##                                                 pump_efficiency)

##(Wm,eff,b_temp,c_temp,Qin_m,Qout_m) = orc.ORC_model(c_power,
##                                                    b_power,
##                                                    turbine_efficiency,
##                                                    pump_efficiency,
##                                                    db_path)
##print("Power output: {:4.2f}kW/(kg/s)".format(Wm))
##print("Thermal efficiency: {:4.4f}".format(eff))
##print("Qin: {:4.2f}kW/(kg/s) Qout: {:4.2f}kW/(kg/s)".format(Qin_m, Qout_m))
##print("Boiler working temp: {:4.2f}C".format(b_temp))
##print("Condenser working temp: {:4.2f}C".format(c_temp))
