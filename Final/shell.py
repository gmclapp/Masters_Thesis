import ORC_Model as orc
import os
import numpy as np
import pandas as pd

np.set_printoptions(precision=3)
# Sets the decimal precision when printing numpy arrays to 3. Note that further
# significant figures are preserved, just not printed.

def find_max_boiler(db_path):
    condenser_pressure = 0.3
    boiler_pressure = 3.0
    turbine_efficiency = 0.9 
    pump_efficiency = 0.9
    max_source_temp = 100
    test_temp = 120
    while test_temp > max_source_temp:
        (Wm,eff,b_temp,c_temp,Qin_m,Qout_m) = orc.ORC_model(condenser_pressure,
                                                            boiler_pressure,
                                                            turbine_efficiency,
                                                            pump_efficiency,
                                                            db_path)
        test_temp = b_temp
        print("T: {:4.2f} deg, P: {:4.2f} MPa".format(b_temp, boiler_pressure))
        boiler_pressure -= 0.01
    print("Power: {:4.2f}kW/(kg/s)\nEfficiency: {:4.2f}" .format(Wm, eff))
    print("Heat in: {:4.2f}kW/(kg/s)\nHeat out: {:4.2f} kW/(kg/s)".format(Qin_m,Qout_m))
    print("Condenser temperature: {:4.2f} deg Celsius\nBoiler temperature: {:4.2f} deg Celsius".format(c_temp,b_temp))
    print("Boiler pressure: {:4.2f} MPa".format(boiler_pressure))
    
def find_best(condenser_pressure, boiler_pressure, turbine_efficiency=0.9,
              pump_efficiency=0.9):
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
                    
    
R245fa_db = '\\R245fa Saturated properties temperature table.csv'
os.chdir("..")# Navigate up a directory
db_path=os.path.abspath(os.curdir)+r"\GHSP study\Additional references"+R245fa_db
# Navigate to the directory containing the working fluid database.

##find_max_boiler(db_path)


condenser_pressure_range = np.linspace(0.1225, 0.5, 25)
# Creates a numpy array with 25 data points between 0.1225 and 0.5.
boiler_pressure_range = np.linspace(0.5, 1.26, 25)
# Max boiler pressure in range determined by earlier numerical analysis.
