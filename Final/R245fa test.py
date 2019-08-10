import CoolProp.CoolProp as CP

print(CP.PropsSI('D', 'T', 298.15, 'P', 101325, 'Nitrogen'))

print(CP.PropsSI('H', 'S', 1800, 'P', 234360, 'R245fa'))
#enthalpy as a given pressure and entropy!
print(CP.PropsSI('H', 'S', 694.9, 'P', 1270, 'R245fa'))
