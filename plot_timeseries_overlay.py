#! /usr/local/bin/python

"""
Created on Mon Aug 22 2016

@author: lgarzio
"""

import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.lines as mlines
import numpy as np
import os
import re

'''
This script is used to overlay timeseries plots of telemetered and recovered data from netCDF or ncml files.
'''

recovered = 'http://opendap.oceanobservatories.org:8090/thredds/dodsC/ooi/lgarzio-marine-rutgers/20160822T055250-CP05MOAS-GL376-03-CTDGVM000-recovered_host-ctdgv_m_glider_instrument_recovered/deployment0001_CP05MOAS-GL376-03-CTDGVM000-recovered_host-ctdgv_m_glider_instrument_recovered.ncml'
telemetered = 'http://opendap.oceanobservatories.org:8090/thredds/dodsC/ooi/lgarzio-marine-rutgers/20160822T055317-CP05MOAS-GL376-03-CTDGVM000-telemetered-ctdgv_m_glider_instrument/deployment0001_CP05MOAS-GL376-03-CTDGVM000-telemetered-ctdgv_m_glider_instrument.ncml'

rec = nc.Dataset(recovered)
tel = nc.Dataset(telemetered)

global fName
head, tail = os.path.split(recovered)
fName = tail.split('.', 1)[0]
title = fName[0:27]
#title = fName.split('_')[1].split('-')[0:4]
#title = title[0] + "-" + title[1] + "-" + title[2] + "-" + title[3]

# Gets the recovered and telemetered time variables and converts to dates
time_rec_var = rec.variables['time']
time_rec_num = time_rec_var[:]
time_rec_num_units = time_rec_var.units
time_rec = nc.num2date(time_rec_num, time_rec_num_units)

time_tel_var = tel.variables['time']
time_tel_num = time_tel_var[:]
time_tel_num_units = time_tel_var.units
time_tel = nc.num2date(time_tel_num, time_tel_num_units)

# Identifies variables to skip when plotting
misc_vars = ['quality', 'string', 'timestamp', 'deployment', 'id', 'provenance', 'qc']
reg_ex = re.compile('|'.join(misc_vars))

sci_vars_rec = [s for s in rec.variables if not reg_ex.search(s)]
sci_vars_tel = [s for s in tel.variables if not reg_ex.search(s)]

for r in sci_vars_rec:
    for t in sci_vars_tel:
        if r == t: # check if r and t are the same variable

            r_var = rec.variables[r]
            r_data = r_var[:]

            t_var = tel.variables[t]
            t_data = t_var[:]

            try:
                y_units = r_var.units
            except AttributeError:
                y_units = ""
                continue

            # get min and max for recovered data
            try:
                r_min = np.nanmin(r_data)
            except TypeError:
                r_min = ""
                continue

            try:
                r_max = np.nanmax(r_data)
            except TypeError:
                r_max = ""
                continue

            # get min and max for telemetered data
            try:
                t_min = np.nanmin(t_data)
            except TypeError:
                t_min = ""
                continue

            try:
                t_max = np.nanmax(t_data)
            except TypeError:
                t_max = ""
                continue

            # set up plot
            fig, ax = plt.subplots()
            plt.grid()
            plt.margins(y=.1, x=.1)

            # create plot of recovered data
            try:
                #plt.plot(time_rec, r_data, 'o', markerfacecolor='none', markeredgecolor='r', lw = .75, label='Recovered')
                rec_plot = plt.plot(time_rec, r_data, 'o', markerfacecolor='none', markeredgecolor='r', lw=.75, ls='-', color='r')
                rec_plot
            except ValueError:
                print 'x and y must be the same size'
                continue

            #overlay plot of telemetered data
            try:
                #plt.plot(time_tel, t_data, 'x', markeredgecolor='b', label='Telemetered')
                tel_plot = plt.plot(time_tel, t_data, 'x', markeredgecolor='b', lw=1.5, ls=':', color='b')
                tel_plot
            except ValueError:
                print 'x and y must be the same size'
                continue

            # Format date axis
            df = mdates.DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_formatter(df)
            fig.autofmt_xdate()

            # Format y-axis to disable offset
            y_formatter = ticker.ScalarFormatter(useOffset=False)
            ax.yaxis.set_major_formatter(y_formatter)

            # Labels
            ax.set_ylabel(rec[r].name + " ("+ y_units + ")")
            ax.set_title(title, fontsize=10)

            # Format legend
            rec_leg = mlines.Line2D([], [], markerfacecolor='none', marker='o', markeredgecolor='r', color='r',
                                    label=("Recovered" + "\n  Max: %f" % r_max + "\n  Min: %f" % r_min))
            rec_tel = mlines.Line2D([], [], marker='x', markeredgecolor='b', ls=':',
                                    label=("Telemetered" + "\n  Max: %f" % t_max + "\n  Min: %f" % t_min))
            ax.legend(handles=[rec_leg, rec_tel],loc='best', fontsize=8)
            #ax.legend(["o: Recovered" + "\n    Max: %f" % r_max + "\n    Min: %f" % r_min +
            #           "\nx: Telemetered" + "\n    Max: %f" % t_max + "\n    Min: %f" % t_min],
            #          loc='best', fontsize=8, markerscale=0, handlelength=0)

            # Save plot
            save_dir = '/Users/lgarzio/Documents/OOI'
            filename = title + "_" + r
            save_file = os.path.join(save_dir, filename)  # create save file name
            plt.savefig(str(save_file),dpi=150) # save figure
            plt.close()