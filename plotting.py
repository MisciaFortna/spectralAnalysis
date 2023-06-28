# @Name: plotting.py
# @Author: Miscia Fortna
# @Date: 28.06.2023
# @Description: module for plotting-related functions
#   - ePlot: creates a figure of energy histogram
#       @Inputs:
#           * dataLib: The Dictionary of Particle Dataframes
#           * particle: Str of Specific Particle to Graph
#           * kwargs:
#               -- bins: Number of Energy Bins (default is 20)
#               -- maxE: Maximum Energy Bin (default is set max)
#               -- minE: Minimum Energy Bin (default is set to 0)
#               -- figdim: pandas fig size (default is set to [15, 10])
#       @Outputs: the figure of the plot
#   - eComp: creates a binned energy figure comparing two surfaces
#       @Inputs
#           * firstLib: initial surface dataframe dictionary
#           * secondLib: second surface dataframe dictionary
#           * particle: Str of Specific Particle to Graph
#           * kwargs:
#               -- bins: Number of Energy Bins (default is 20)
#               -- maxE: Maximum Energy Bin (default is set max)
#               -- minE: Minimum Energy Bin (default is set to 0)
#               -- figdim: pandas fig size (default is set to [15, 10])
import pandas as pd
import csv
import math
import matplotlib.pyplot as plt

# bins
# maxE
# minE
# figdim
def ePlot(dataLib, particle, **kwargs):
    defaultKwargs = { 'bins': 20, 'maxE': dataLib[particle]['energy'].max(), 'minE': 0, 'figdim': [15,10] }
    kwargs = { **defaultKwargs, **kwargs }
    bins = kwargs['bins']
    binList = [0] * (bins + 1)
    maxE = kwargs['maxE']
    minE = kwargs['minE']
    step = (maxE-minE) / bins
    figdim = kwargs['figdim']
    for j in range(0,bins + 1):
        binList[j] = step * j
    plot = dataLib[particle].plot.hist(column=['energy'], bins = binList, xticks = binList, xlim = [minE, maxE], xlabel = 'Energy (MeV)', figsize = figdim, grid = 1)
    fig = plot.get_figure()
    return fig

# returns fig
def eComp(firstLib, secondLib, particle, **kwargs):
    defaultKwargs = { 'bins': 20, 'maxE': 0, 'minE': 0, 'figdim': [15,10] }
    kwargs = { **defaultKwargs, **kwargs }
    
    if particle == "frag":

        difference = list(set(firstLib.keys()) - set(secondLib.keys())
        for value in difference:
            firstLib.pop(value)

        difference = list(set(secondLib.keys()) - set(firstLib.keys())
        for value in difference:
            secondLib.pop(value)

        fragList = []
        dataSet = []
    
        for key in firstLib.keys():
            if key.startswith('10000'):
                fragList.append(key)
    
        for i in fragList:
            dataSet.append(firstLib[i])
    
        fragNumer = pd.concat(dataSet, ignore_index = 1)
    
        for i in fragList:
            dataSet.append(secondLib[i])
    
        fragDenom = pd.concat(dataSet, ignore_index = 1)
        together = {'Surface 1' : fragNumer['energy'], 'Surface 2' : fragDenom['energy'] }
    
    else:
        together = {'Surface 1' : firstLib[particle]['energy'], 'Surface 2' : secondLib[particle]['energy'] }
    
    df = pd.DataFrame(data = together)
    bins = kwargs['bins']
    binList = [0] * (bins+1)
    if kwargs['maxE'] == 0:
        if df['Surface 1'].max() > df['Surface 2'].max():
            maxE = df['Surface 1'].max()
        else:
            maxE = df['Surface 2'].max()
    else:
        maxE = kwargs['maxE']
    minE = kwargs['minE']
    step = (maxE - minE) / bins
    for i in range(bins+1):
        binList[i] = round(step * i,2)

    ax = df.plot.hist(bins = binList, xticks = binList, xlim = [0, maxE], figsize = figdim, alpha = 0.5, xlabel = "Energy in MeV")
    fig = ax.get_figure()
    return fig
