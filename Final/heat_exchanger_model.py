import csv
import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import misc_functions as mf

def LMTD(Th1, Th2, Tc1, Tc2):
    '''Returns the log mean temperature difference given the entry and exit
    temperatures of the hot fluid, Th1 and Th2, and the entry and exit
    temperatures of the cool fluid, Tc1 and Tc2.'''

    log_mean_temp_diff = ((Th2-Tc2)-(Th1-Tc1))/math.log(((Th2-Tc2)/(Th1-Tc1)))
    return(log_mean_temp_diff)

def feedwater_exit_temp(Th1,c,Q):
    '''Returns the feedwater exit temp given the entry temp, the specific heat
    capacity, and the heat transfer per unit mass flow rate required.'''
    
    Th2 = -1*(Q/c - Th1)
    return(Th2)

def tube_in_shell(dT, Q, U = 850):
    '''Returns the required heat exchange area given the heat transfer required,
    The temperature difference between the two working fluids, and the overall
    heat transfer coefficient.'''

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
    pass

