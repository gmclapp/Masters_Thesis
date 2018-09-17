import csv
import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import database_functions as dbf

whr_mass_flow_rate = 1 # kg/s
feedwater_mass_flow_rate = 2.25 # kg/s
feedwater_density = 1.08 # kg/L
F = 1.0 # LMTD correction factor for boiler

Th245 = 90 # Celsius
Tc245 = 60 # Celsius
C245 = 1.302 # Heat capacity KJ/(kg K) @atm press & 15.14 deg C
Cfeed = 3.3488 # Heat capacity KJ/(kg K) @atm press & 26.7 deg C
Thfeedwater = 97.5 # Temperature of automotive feedwater

whr_efficiency = 0.15 # From previous study

# Heat energy required to raise working fluid temperature.
q_in = whr_mass_flow_rate*C245*(Th245 - Tc245)
print("Heat transfer in: ", q_in) # kW

W_out = q_in * whr_efficiency
print("Work out: ", W_out)

# Assuming that the heat transferred into the working fluid is 100% of the heat
# transferred out of the feedwater, the temperature drop of the feedwater can
# be found.

dT = q_in/(feedwater_mass_flow_rate*Cfeed)
print("dT: ", dT)
Tcfeedwater = Thfeedwater - dT

# LMTD Method
dTm = ((dT) - (Th245 - Tc245))/math.log(dT/(Th245 - Tc245))
print("Mean temperature difference: ", dTm)

# In the future, the heat transfer coefficient should be calculated. for now,
# table 10-1 form "Heat Transfer" by J.P. Holman was used Umin = 850 W/(m2 C),
# Umax = 1400 W/(m2 C).

U = 850 # W/(m2 C)
A = q_in*1000/(U*dTm) # square meters
print("Boiler heat exchange area: ", A)

# Calculate the number of tubes in shell based on tube diameter and tube and
# and shell exchanger length.

L = 0.25 # meters
d = 0.003 # diameter of tubes in meters
circ = A/L # circumference of all tubes
n = circ/(math.pi*d)

print("Number of tubes: ", n)

