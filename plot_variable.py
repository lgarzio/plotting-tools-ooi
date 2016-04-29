#! /usr/local/bin/python

"""
Created on Mon Feb 15 2016

@author: lgarzio
"""

import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import numpy as np

'''
This script is used to generate a simple timeseries plot of one variable from netCDF or ncml files.
'''

ncml = 'http://opendap-devel.ooi.rutgers.edu:8090/thredds/dodsC/first-in-class/Global_Irminger_Sea/GI02HYPM/05-VEL3DL000/recovered_wfp/GI02HYPM-WFP02-05-VEL3DL000-vel3d_l_wfp_instrument_recovered-recovered_wfp/GI02HYPM-WFP02-05-VEL3DL000-vel3d_l_wfp_instrument_recovered-recovered_wfp.ncml'
f = nc.Dataset(ncml)

global fName
head, tail = os.path.split(ncml)
fName = tail.split('.', 1)[0]

# Gets the time variable and converts to a date
time_var = f.variables['time']
time_num = time_var[:]
time_num_units = time_var.units
time = nc.num2date(time_num, time_num_units)

for v in f.variables:
    print(v)

y_var = f.variables['vel3d_l_upward_velocity_descending']
y_data = f.variables['vel3d_l_upward_velocity_descending'][:]
y_units = f.variables['vel3d_l_upward_velocity_descending'].units
y_name = f.variables['vel3d_l_upward_velocity_descending'].name
ymin = np.nanmin(y_data)
ymax = np.nanmax(y_data)

fig, ax = plt.subplots()
plt.grid()
plt.ylim([-1,1])

plt.scatter(time, y_data, c='r', marker='o', lw = .25)

# Format date axis
df = mdates.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(df)
fig.autofmt_xdate()

# Labels
ax.set_ylabel("vel3d_l_upward_velocity_descending" + " ("+ y_units + ")")
ax.set_title(fName, fontsize=9)
ax.legend(["Max: %f" % ymax + "\nMin: %f" % ymin], loc='best', fontsize=8)

save_dir = '/Users/lgarzio/Documents'
filename = fName + "_" + y_name
save_file = os.path.join(save_dir, filename)  # create save file name
plt.savefig(str(save_file),dpi=150) # save figure
plt.close()