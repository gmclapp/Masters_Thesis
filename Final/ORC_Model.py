import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import misc_functions as mf
import sanitize_inputs as si

def boiler_model():
    pass
def condenser_model():
    pass
def turbine_model():
    pass
def pump_model():
    pass
def ORC_model():
    '''This function takes a working pressure for a condenser and boiler, an
    efficiency for a pump and turbine, and outputs the work per unit mass flow
    and thermal efficiency for a generic ORC, as well as the working temperature
    and enthalpy at each of the four fixed states which can then be used in the
    models for the individual major components.'''
    pass

#------Main------#
if __name__ == '__main__':
    '''Manual entry begins here.'''
    condenser_pressure = si.get_real_number("Enter condenser pressure.\n>>>")
    boiler_pressure = si.get_real_number("Enter boiler pressure.\n>>>")
    ORC_model()
else:
    pass
