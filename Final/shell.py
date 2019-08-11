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

def find_max_boiler(condenser_pressure, boiler_pressure, turbine_efficiency, pump_efficiency, max_source_temp,c_h,m_ORC,m_h, db_path):

    test_temp = 0
    b_temp = max_source_temp-0.1
    while test_temp < b_temp:
        (Wm,eff,b_temp,c_temp,Qin_m,Qout_m) = orc.ORC_model(condenser_pressure,
                                                            boiler_pressure,
                                                            turbine_efficiency,
                                                            pump_efficiency,
                                                            db_path)

        test_temp = heatex.feedwater_exit_temp(max_source_temp,c_h,Qin_m,m_ORC,m_h)
        
        print("T: {:4.2f} deg, P: {:4.2f} MPa".format(test_temp, boiler_pressure))
        boiler_pressure -= 0.01
    print("Power: {:4.2f}kW/(kg/s)\nEfficiency: {:4.2f}" .format(Wm, eff))
    print("Heat in: {:4.2f}kW/(kg/s)\nHeat out: {:4.2f} kW/(kg/s)".format(Qin_m,Qout_m))
    print("Condenser temperature: {:4.2f} deg Celsius\nBoiler temperature: {:4.2f} deg Celsius".format(c_temp,b_temp))
    print("Boiler pressure: {:4.2f} MPa".format(boiler_pressure))
    
R245fa_db = '\\R245fa Saturated properties temperature table.csv'

db_upper_pressure_limit = 3.651
db_lower_pressure_limit = 0.00127

os.chdir("..")# Navigate up a directory
db_path=os.path.abspath(os.curdir)+r"\GHSP study\Additional references"+R245fa_db
# Navigate to the directory containing the working fluid database.

p_boiler_max = si.get_real_number("Enter the boiler working pressure upper limit (MPa):\n",upper=db_upper_pressure_limit,lower=db_lower_pressure_limit)
p_boiler_min = si.get_real_number("Enter the boiler working pressure lower limit (MPa):\n",upper=p_boiler_max,lower=db_lower_pressure_limit)

p_condenser_max = si.get_real_number("Enter the condenser working pressure upper limit (MPa):\n",upper=p_boiler_min,lower=db_lower_pressure_limit)
p_condenser_min = si.get_real_number("Enter the condenser working pressure lower limit (MPa)(0.123 corresponds to a 20C working temp):\n",upper=p_condenser_max,lower=db_lower_pressure_limit)
turbine_efficiency = si.get_real_number("Enter isentropic turbine efficiency (0-1):\n",upper=1,lower=0)# Study value = 0.787
pump_efficiency = si.get_real_number("Enter isentropic pump efficiency (0-1):\n",upper=1,lower=0)# Study value = 0.9

max_source_temp = si.get_real_number("Enter the maximum heat source temperature:\n")
source_specific_heat = si.get_real_number("Enter the specific heat of the heat source fluid (kJ/kgK)",lower=0)
# 3.7682 kJ/kgK for 5050 water/glycol mixture
m_245 = si.get_real_number("Enter the mass flow rate of the ORC working fluid (kg/s)",lower=0)
m_source = si.get_real_number("Enter the mass flow rate of the source working fluid (kg/s)",lower=0)

# Creates a numpy array with 25 data points between p_condenser_min and p_condenser_max.
##condenser_pressure_range = np.linspace(p_condenser_min, p_condenser_max, 25)
##boiler_pressure_range = np.linspace(p_boiler_min, p_boiler_max, 25)

##condenser_pressure = 0.13
##boiler_pressure = 1.26
##turbine_efficiency = 0.787
##pump_efficiency = 0.9
##max_source_temp = 97.5

find_max_boiler(p_condenser_min,
                p_boiler_max,
                turbine_efficiency,
                pump_efficiency,
                max_source_temp,
                source_specific_heat,
                m_245,
                m_source,
                db_path)

user = None
while(1):
    user = input()
    if user == 'q':
        break
    else:
        pass

##print("Power output: {:4.2f}kW/(kg/s)".format(Wm))
##print("Thermal efficiency: {:4.4f}".format(eff))
##print("Qin: {:4.2f}kW/(kg/s) Qout: {:4.2f}kW/(kg/s)".format(Qin_m, Qout_m))
##print("Boiler working temp: {:4.2f}C".format(b_temp))
##print("Condenser working temp: {:4.2f}C".format(c_temp))
