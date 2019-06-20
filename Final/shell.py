import ORC_Model as orc
import os

R245fa_db = '\\R245fa Saturated properties temperature table.csv'
os.chdir("..")# Navigate up a directory
db_path=os.path.abspath(os.curdir)+r"\GHSP study\Additional references"+R245fa_db
# Navigate to the directory containing the working fluid database.

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
