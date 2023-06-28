# @Name: specReadLib.py
# @Author: Miscia Fortna
# @Date: 15.06.2023
# @Description: Library of Spectral Reading Functions from Previous Scripts
#   - phsp_2_csv: converts phsp file to csv
#       @Inputs: fName: File Name (sans file type)
#       @Outputs: A Saved CSV File
#   - txt_2_csv: converts txt file to csv (NB txt file MUST BE COMMA DELIM AT BEGINNING OF LINES)
#       @Inputs: fName: File Name (sans file type)
#       @Outputs: A Saved CSV File
#   - read_val: creates a dictionary of particle information
#       @Inputs:
#           * fName: File Name of CSV (sans file type)
#           * kwargs: 
#               -- particles: Str List of Particle ID Numbers
#               -- save: Bool Value if Save or Not
#       @Outputs:
#           * Returned Dictionary
#           * Collection of Particle-Filtered CSV Files
#   - ePlot: creates a plot of energies
#       @Inputs:
#           * dataLib: The Dictionary of Particle Dataframes
#           * particle: Str of Specific Particle to Graph
#           * kwargs:
#               -- bins: Number of Energy Bins (default is 20)
#               -- maxE: Maximum Energy Bin (default is set max)
#               -- minE: Minimum Energy Bin (default is set to 0)
#               -- figdim: pandas fig size (default is set to [15, 10])
#       @Outputs: the figure of the plot
#   - degRatio : returns dataframe of ratio between neutrons and other particles
#       @Inputs:
#           * dataLib: Dictionary of Particle Dataframes
#           * box: Height of Dosimeter Box for Flux
#           * degBins: Number of Degree Bins
#           * center: The Center Position Along Beam Line
#       @Outputs: Dataframe of Ratio Data
import argparse
import pandas as pd
import csv
import math
import matplotlib.pyplot as plt

def phsp_2_csv(fName):

    input_file = fName + ".phsp"
    output_file = fName + ".csv"

    with open(input_file) as f, NamedTemporaryFile("w", dir=".", delete = False) as temp:

        for line in f:
            lineTemp = ' ' + line.strip()
            lineTemp = re.sub("\s+", ",", lineTemp)
            print(lineTemp, file=temp)

        with open(temp.name, 'r') as infile:
            stripped = (line.strip() for line in infile)
            lines = (line.split(",") for line in stripped if line)
            with open(output_file, 'w') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(('empty','x','y','z','cos(x)','cos(y)','energy','weight','particle','neg_cos(z)','first_particle'))
                writer.writerows(lines)
    edit_output = pd.read_csv(output_file, index_col = False)
    edit_output.pop('empty')
    edit_output.to_csv(output_file, index = False)

def txt_2_csv(fName):
    input_file = fName + ".txt"
    output_file = fName + ".csv"
    with open(input_file, 'r') as infile:
        stripped = (line.strip() for line in infile)
        lines = (line.split(",") for line in stripped if line)
        with open(output_file, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(('empty','x','y','z','cos(x)','cos(y)','energy','weight','particle','neg_cos(z)','first_particle'))
            writer.writerows(lines)
    edit_output = pd.read_csv(output_file, index_col = False)
    edit_output.pop('empty')
    edit_output.to_csv(output_file, index = False)

def read_val(fName,**kwargs):
    defaultKwargs = { 'save': False, 'particles': ['default']}
    kwargs = { **defaultKwargs, **kwargs }
    input_file = fName + ".csv"
    data = pd.read_csv(input_file, index_col = False)
    if kwargs['particles'] == ['default']:
        particles = data['particle'].unique().tolist()
        for i in range(len(particles)):
            particles[i] = str(particles[i])
    else:
        particles = kwargs['particles']
    dataLib = {}

    for i in particles:
        data_temp = data[data['particle']== int(i)]
        data_temp = data_temp.reset_index()
        data_temp.pop('index')
        dataLib[i] = data_temp

    if kwargs['save']:
        for i in particles:
            output = fName + "_" + i + ".csv"
            dataLib[i].to_csv(output, index = False)
    else:
        return dataLib

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

def degRatio(dataLib, box, degBins, center):
    particles = list(dataLib.keys())
    dataSet = []

    for i in particles:
        dataLib[i] = dataLib[i][dataLib[i]['y'] <= (box / 2)]
        dataLib[i] = dataLib[i][dataLib[i]['y'] >= -1 *  (box / 2)]
        dataLib[i] = dataLib[i].reset_index() # Adds new index tared
        dataLib[i].pop('index')            # Removes previous index
        if i != '2112':
            dataSet.append(dataLib[i])

    extraParticles = pd.concat(dataSet, ignore_index = True) # combines data frames into single data frame

    bins = list(range(0, 370, degBins)) # don't know why this binning works

    denom = [0] * len(bins) # init of denominator of ratio (extra particles)

    numer = [0] * len(bins) # init of numerator of ratio (neutrons)

    angleSet = [0] * len(extraParticles) # init set of angles for entering into data frame

    for i in range(len(extraParticles)):
        zPos = extraParticles['z'][i] + center
        xPos = extraParticles['x'][i]
    
        angle = math.atan2(xPos,zPos) * 180 / math.pi

        if xPos < 0:
            angleSet[i] = angle + 360 # necessary for the bottom half of the circle
        else:
            angleSet[i] = angle

    extraParticles['angle'] = angleSet

    angleSet = [0] * len(dataLib['2112'])

    for i in range(len(dataLib['2112'])):
        zPos = dataLib['2112']['z'][i] + center
        xPos = dataLib['2112']['x'][i]
    
        angle = math.atan2(xPos,zPos) * 180 / math.pi

        if xPos < 0:
            angleSet[i] = angle + 360
        else:
            angleSet[i] = angle

    dataLib['2112']['angle'] = angleSet

    for i in range(1,37): # counts the number of particles in the given bin
        denom[i-1] = len(extraParticles[extraParticles['angle'] < bins[i]]) - len(extraParticles[extraParticles['angle'] < bins[i-1]])
        numer[i-1] = len(dataLib['2112'][dataLib['2112']['angle'] < bins[i]]) - len(dataLib['2112'][dataLib['2112']['angle'] < bins[i-1]])

    del denom[-1] # for some reason gives an additional element but I am too afraid to change the range
    del numer[-1]

    ratio = [0] * 36

    for i in range(36):

        ratio[i] = numer[i] / denom[i]

    ratioData = pd.DataFrame({'bins':list(range(0,360, degBins)), 'frequency':ratio})

    return ratioData

    # Histogram
    #titleValue = fName
    #plot = ratioData.plot.bar(x = 'bins', y = 'frequency', position = 0, width = 1, grid = True, title = titleValue, figsize = [10, 10])
    #fig = plot.get_figure()
