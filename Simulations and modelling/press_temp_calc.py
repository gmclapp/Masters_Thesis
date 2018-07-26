import csv
import math
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import database_functions as dbf

#----------Main----------#
fig = plt.figure()
fig1 = plt.figure()
fig2 = plt.figure()
fig3 = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax1 = fig1.add_subplot(111, projection='3d')
ax2 = fig2.add_subplot(111, projection='3d')
ax3 = fig3.add_subplot(111, projection='3d')

c_press = np.linspace(0.1225, 0.5, 25)
b_press = np.linspace(0.5,1,25)

X = []
X2 = []
Y = []
Y2 = []
Z = []
Z2 = []


R245fa_db = 'R245fa Saturated properties temperature table.csv'
db_path = 'H:\\WIP\\12343 - Research & Development\\Issue #251 - Rankine cycle research\\Additional references'

out_db = "output.csv"
out_file = open("%s/%s" %(db_path, out_db), mode = 'w',newline='')
wrt = csv.writer(out_file)
wrt.writerow([
    "Boiler pressure (MPa)",
    "Boiler temperature (C)",
    "Condenser pressure (MPa)",
    "Condenser temperature (C)",
    "Power out (Watts per unit mass flow rate (kg/s)",
    "efficiency"])

for xs in c_press:
    for ys in b_press:
        boiler_pressure = ys
        condenser_pressure = xs

        temp_col = 0 # Degrees Celsius
        press_col = 1 # MPa
        v_col = 3 # Specific volume of vapor m3/kg
        hl_col = 4 # Enthalpy of saturated liquid kJ/kg
        hv_col = 5 # Enthalpy of saturated vapor kJ/kg
        sl_col = 6 # Entropy of saturated liquid kJ/(kgK)
        sv_col = 7 # Entropy of saturated vapor kJ/(kgK)

        # Fix states with specified pressures
        p1 = boiler_pressure
        p4 = boiler_pressure

        file = open("%s/%s" %(db_path, R245fa_db), mode = 'r', newline='')
        x1, y1, x2, y2 = dbf.vlookup(file, p1, press_col, temp_col)
        boiler_temp = dbf.interpolate(x1, y1, x2, y2, p1)

        file.seek(0)
        
        p2 = condenser_pressure
        p3 = condenser_pressure

        x1, y1, x2, y2 = dbf.vlookup(file, p2, press_col, temp_col)
        condenser_temp = dbf.interpolate(x1, y1, x2, y2, p2)

        file.seek(0)

        x1, y1, x2, y2 = dbf.vlookup(file, p1, press_col, hv_col)
        h1 = dbf.interpolate(x1, y1, x2, y2, p1)

        file.seek(0)

        x1, y1, x2, y2 = dbf.vlookup(file, p1, press_col, sv_col)
        s1 = dbf.interpolate(x1, y1, x2, y2, p1)
        s2 = s1

        file.seek(0)

        # Calculate the quality of state 2
        # First find the liquid and vapor entropy at the condenser pressure
        x1, y1, x2, y2 = dbf.vlookup(file, p2, press_col, sl_col)
        s2L = dbf.interpolate(x1, y1, x2, y2, p2)

        file.seek(0)

        x1, y1, x2, y2 = dbf.vlookup(file, p2, press_col, sv_col)
        s2v = dbf.interpolate(x1, y1, x2, y2, p2)
        file.seek(0)

        try:
            qual_2 = (s2 - s2L)/(s2v - s2L)
        except ZeroDivisionError:
            qual_2 = 0
        except RuntimeWarning:
            qual_2 = 0

        # Note that evaporating enthalpy is equal to the difference between the enthalpy
        # of a saturated vapor and the enthalpy of a saturated liquid at a given
        # temperature or pressure.

        x1, y1, x2, y2 = dbf.vlookup(file, p2, press_col, hl_col)
        h2L = dbf.interpolate(x1, y1, x2, y2, p2)
        file.seek(0)

        x1, y1, x2, y2 = dbf.vlookup(file, p2, press_col, hv_col)
        h2v = dbf.interpolate(x1, y1, x2, y2, p2)

        hLv = h2v - h2L
        file.seek(0)

        h2 = h2L + (qual_2*hLv)

        x1, y1, x2, y2 = dbf.vlookup(file, p2, press_col, hl_col)
        h3 = dbf.interpolate(x1, y1, x2, y2, p2)
        file.seek(0)

        x1, y1, x2, y2 = dbf.vlookup(file, p2, press_col, v_col)
        v3 = dbf.interpolate(x1, y1, x2, y2, p2)
        file.seek(0)

        h4 = h3 + v3*(p4-p3)

        W_m = h1-h2-h4+h3 # Watts of power per kg/s of mass flow rate

        efficiency = ((h1-h2) - (h4-h3))/(h1 - h4)
        
        X.append(boiler_pressure)
        X2.append(boiler_temp)
        
        Y.append(condenser_pressure)
        Y2.append(condenser_temp)
        
        Z.append(W_m)
        Z2.append(efficiency)

file.close()
out_file = open("%s/%s" %(db_path, out_db), mode = 'w',newline='')

for i in range(len(X)):
    wrt.writerow([X[i], X2[i], Y[i], Y2[i], Z[i], Z2[i]])
out_file.close()

ax.set_xlabel("Boiler Pressure (MPa)")
ax.set_ylabel("Condenser Pressure (MPa)")
ax.set_zlabel("Power output per unit mass flow rate (Watts)")
ax.scatter(X, Y, Z)

ax1.set_xlabel("Boiler Pressure (MPa)")
ax1.set_ylabel("Condenser Pressure (MPa)")
ax1.set_zlabel("Efficiency")
ax1.scatter(X, Y, Z2)

ax2.set_xlabel("Boiler Temperature (C)")
ax2.set_ylabel("Condenser Temperature (C)")
ax2.set_zlabel("Power output per unit mass flow rate (Watts)")
ax2.scatter(X2, Y2, Z, color='r')

ax3.set_xlabel("Boiler Temperature (C)")
ax3.set_ylabel("Condenser Temperature (C)")
ax3.set_zlabel("Efficiency")
ax3.scatter(X2, Y2, Z2, color='r')

plt.show()
