#! /usr/local/bin/python

"""
Created on Wed Apr 6 2016

@author: lgarzio
"""

# quick plot of OOI SPKIR data

import netCDF4 as nc
import matplotlib.pyplot as plt
import os

ncml = 'http://opendap-devel.ooi.rutgers.edu:8090/thredds/dodsC/first-in-class/Global_Irminger_Sea/GI01SUMO/05-SPKIRB000/recovered_host/GI01SUMO-SBD11-05-SPKIRB000-spkir_abj_dcl_instrument_recovered-recovered_host/GI01SUMO-SBD11-05-SPKIRB000-spkir_abj_dcl_instrument_recovered-recovered_host.ncml?spkir_abj_cspp_downwelling_vector[0:1:1000][0:1:6]'
f = nc.Dataset(ncml)

global fName
head, tail = os.path.split(ncml)
fName = tail.split('.', 1)[0]

spkir = f.variables['spkir_abj_cspp_downwelling_vector'][:]
spkir_units = f.variables['spkir_abj_cspp_downwelling_vector'].units
y_name = f.variables['spkir_abj_cspp_downwelling_vector'].name
#wav420 = spkir[:,0]
spkir = spkir.T #transpose the array
x_axis = [412,443,490,510,555,620,683]

fig, ax = plt.subplots()
plt.grid()
#plt.ylim([-1,1])

plt.plot(x_axis,spkir)

# Labels
ax.set_ylabel("spkir_abj_cspp_downwelling_vector" + " ("+ spkir_units + ")", fontsize=9)
ax.set_xlabel("Wavelength (nm)", fontsize=9)
ax.set_title(fName, fontsize=9)

save_dir = '/Users/lgarzio/Documents/OOI/DataReviews/firstinclass/GI01SUMO'
filename = fName + "_" + y_name
save_file = os.path.join(save_dir, filename)  # create save file name
plt.savefig(str(save_file),dpi=150) # save figure
plt.close()