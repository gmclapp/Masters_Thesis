import ORC_Model as orc

condenser_pressure = 0.3
boiler_pressure = 0.7
turbine_efficiency = 0.9
pump_efficiency = 0.9

while boiler_pressure < 1:
    (Wm,eff,b_temp,c_temp,Qin_m,Qout_m) = orc.ORC_model(condenser_pressure,
                                                boiler_pressure,
                                                turbine_efficiency,
                                                pump_efficiency)
    boiler_pressure += 0.1
