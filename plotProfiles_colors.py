#! /usr/local/bin/python
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re
import os
import datetime as dt
import matplotlib.cm as cm


def plot_profiles(x, y, t, args):
    # args = (xName, yName, fName, saveDir)
    xD = x[:]
    yD = y[:]

    fig,ax = plt.subplots()
    minorLocator = ticker.AutoMinorLocator()

#    ax.plot(xD, yD, 'ro')
    colors = cm.rainbow(np.linspace(0,1, len(t)))
    ax.scatter(xD, yD, c = colors, edgecolor='None')
    
    # Image size
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 12
    fig_size[1] = 8.5
    plt.rcParams["figure.figsize"] = fig_size

    # setup axes
    ax.xaxis.set_minor_locator(minorLocator)
    xax = ax.get_xaxis().get_major_formatter()

    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)
    plt.grid()
    plt.gca().invert_yaxis()

    ax.set_xlabel(args[0] + " (" + x.units + ")") # x label
    ax.set_ylabel(args[1] + ' (' + y.units + ')') # y label
    ax.set_title('Depth Profiles: ' + args[2] + "\n" + args[1]) # title
    sName = str(args[3]) + args[2] + ".png"
    print sName
    plt.savefig(sName,dpi=100) # save figure
    plt.close()


saveDir = '/Users/lgarzio/Documents/OOI/DataReviews/2016_2_17_westcoast/CP05MOAS/profiles/'

urls = ['http://opendap-devel.ooi.rutgers.edu:8090/thredds/dodsC/ufs-west/Coastal_Pioneer/CP05MOAS/03-CTDGVM000/recovered_host/CP05MOAS-GL379-03-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host/CP05MOAS-GL379-03-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host.ncml',
        'http://opendap-devel.ooi.rutgers.edu:8090/thredds/dodsC/ufs-west/Coastal_Pioneer/CP05MOAS/03-CTDGVM000/recovered_host/CP05MOAS-GL376-03-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host/CP05MOAS-GL376-03-CTDGVM000-ctdgv_m_glider_instrument_recovered-recovered_host.ncml']


#seasons = {'winter_2015': [dt.datetime(2014,12,1,0,0,0), dt.datetime(2015,3,1,0,0,0)],
#           'spring_2015': [dt.datetime(2015,3,1,0,0,0), dt.datetime(2015,6,1,0,0,0)],
#           'summer_2015': [dt.datetime(2015,6,1,1,0,0), dt.datetime(2015,9,1,1,0,0)],
#           'fall_2015': [dt.datetime(2015,9,1,0,0,0), dt.datetime(2015,12,1,0,0,0)]}

# pressures = {'ctdbp_cdef_instrument_recovered': 'ctdbp_seawater_pressure',
#              'ctdbp_cdef_dcl_instrument_recovered': 'pressure',
#              'ctdbp_cdef_dcl_instrument-': 'pressure',
#              'ctdgv_m_glider_instrument-': 'sci_water_pressure',
#              'ctdgv_m_glider_instrument_recovered': 'sci_water_pressure',
#              'ctdpf_j_cspp_instrument_recovered': 'pressure',
#              'ctdpf_j_cspp_instrument-': 'pressure',
#              'ctdpf_ckl_wfp_instrument_recovered': 'ctdpf_ckl_seawater_pressure',
#              'ctdpf_ckl_wfp_instrument-': 'ctdpf_ckl_seawater_pressure'}

# streamKeys = list(pressures.keys())
# reStream = re.compile('|'.join(streamKeys))
# yVars = [s for s in yVars if not reV.search(s)]

datastrs = ['time', 'date', 'provenance', 'counts', 'volts', 'qc', 'deployment', 'timestamp','id',
            '_qc_executed', '_qc_results', 'pressure', 'lat', 'lon', 'depth', 'obs', 'm_present',
            'sig', 'ref', 'phase', 'amp', 'rph']

reV = re.compile('|'.join(datastrs))

for url in urls:
    print url
    f = nc.Dataset(url)
    fN = f.id
    y = f.variables['sci_water_pressure_dbar']
    yN = 'sci_water_pressure_dbar'
    t = f.variables['time']
    
    varList = []
    for varNum in f.variables:
        varList.append(str(varNum))

    xVars = [s for s in varList if not reV.search(s)]

    for xN in xVars:
        x = f.variables[xN]
        fName = fN + '_profiles_' + xN
        plotArgs = (xN, yN, fName, saveDir)
        plot_profiles(x, y, t, plotArgs)
