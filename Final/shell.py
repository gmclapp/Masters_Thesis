import ORC_Model as orc
import os

R245fa_db = '\\R245fa Saturated properties temperature table.csv'
os.chdir("..")# Navigate up a directory
db_path=os.path.abspath(os.curdir)+r"\GHSP study\Additional references"+R245fa_db
# Navigate to the directory containing the working fluid database.

condenser_pressure = 0.3
boiler_pressure = 0.7
turbine_efficiency = 0.9
pump_efficiency = 0.9
max_source_temp = 100
test_temp = 0

while test_temp < max_source_temp:
    (Wm,eff,b_temp,c_temp,Qin_m,Qout_m) = orc.ORC_model(condenser_pressure,
                                                        boiler_pressure,
                                                        turbine_efficiency,
                                                        pump_efficiency,
                                                        db_path)
    test_temp = b_temp
    boiler_pressure += 0.01
