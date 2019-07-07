import csv
import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import misc_functions as mf

def tube_in_shell(Th245=90,Tc245=60):
    '''Returns the required heat exchanger area in square meters to
    achieve the boiler and condenser working temperatures specified in
    degrees Celsius.

    Uses a mass flow rate of 1kg/s for both working fluids and assumes R245fa
    for the ORC working fluid and a 50/50 water glycol mix for the heat
    source working fluid.'''
    
    whr_mass_flow_rate = 1 # kg/s
    feedwater_mass_flow_rate = 1 # kg/s 2.25 is common
    feedwater_density = 1.08 # kg/L
    F = 1.0 # LMTD correction factor for boiler

##    Th245 = 90 # Celsius
##    Tc245 = 60 # Celsius
    C245 = 1.302 # Heat capacity of R245 KJ/(kg K) @atm press & 15.14 deg C
    Cfeed = 3.3488 # Heat capacity of water/glycol KJ/(kg K) @atm press & 26.7 deg C
    Thfeedwater = 97.5 # Temperature of automotive feedwater

    whr_efficiency = 0.1366 # From previous study

    # Heat energy required to raise working fluid temperature.
    q_in = whr_mass_flow_rate*C245*(Th245 - Tc245)
    print("Heat transfer in: {:4.2f}kW".format(q_in)) # kW

    W_out = q_in * whr_efficiency
    print("Work out: {:4.2f}kW".format(W_out))

    # Assuming that the heat transferred into the working fluid is 100% of the heat
    # transferred out of the feedwater, the temperature drop of the feedwater can
    # be found.

    dT = q_in/(feedwater_mass_flow_rate*Cfeed)
    print("dT: {:4.2f}C".format(dT))
    Tcfeedwater = Thfeedwater - dT

    # LMTD Method
    print("245 in: {:4.2f}C\n245 out: {:4.2f}C\nFeed in: {:4.2f}C\nFeed out: {:4.2f}C".format(Tc245,Th245,Thfeedwater,Tcfeedwater))
    dTm = ((Tcfeedwater-Th245) - (Tc245-Th245)) / math.log((Tcfeedwater-Th245)/(Thfeedwater-Tc245))
    print("Mean temperature difference: {:4.2f}C".format(dTm))

    # In the future, the heat transfer coefficient should be calculated. for now,
    # table 10-1 form "Heat Transfer" by J.P. Holman was used Umin = 850 W/(m2 C),
    # Umax = 1400 W/(m2 C).

    U = 850 # W/(m2 C)
    A = q_in*1000/(U*dTm) # square meters
    print("Boiler heat exchange area: {:4.2f}m^2".format(A))

    # Calculate the number of tubes in shell based on tube diameter and tube and
    # and shell exchanger length.

    L = 0.25 # meters
    d = 0.003 # diameter of tubes in meters
    circ = A/L # circumference of all tubes
    n = math.ceil(circ/(math.pi*d))

    print("Number of tubes: ", n)

if __name__ == "__main__":
    tube_in_shell()

