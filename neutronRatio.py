# @Name: neutronRatio.py
# @Author: Miscia Fortna
# @Date: 14.06.2023
# @Description: script to obtain a histogram of the ratio of neutrons to extra particles at a given degree bin
import argparse
import pandas as pd
import csv
import math
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description = 'script for neutron to photon+proton ratio') 
parser.add_argument('-n',"--file_name", help = "input file (sans filetype)")
args = parser.parse_args()

inputFile = args.file_name + ".csv"
outputIMG = args.file_name + "_bar.png"

data = pd.read_csv(inputFile, index_col = False)

# Photon
data_22 = data[data['particle']== 22] # Filters for Photons
data_22 = data_22[data_22['y']<=5]    # Filters for y-values below 5 cm
data_22 = data_22[data_22['y']>=-5]   # Filters for y-values above -5 cm

data_22 = data_22.reset_index() # Adds new index tared
data_22.pop('index')            # Removes previous index

# Neutron
data_2112 = data[data['particle']== 2112]
data_2112 = data_2112[data_2112['y']<=5]
data_2112 = data_2112[data_2112['y']>=-5]

data_2112 = data_2112.reset_index()
data_2112.pop('index')

# Proton
data_2212 = data[data['particle']== 2212]
data_2212 = data_2212[data_2212['y']<=5]
data_2212 = data_2212[data_2212['y']>=-5]

data_2212 = data_2212.reset_index()
data_2212.pop('index')

# Extra Particles

dataSet = [data_22, data_2212] # set of data frames for extra particles

extraParticles = pd.concat(dataSet, ignore_index = True) # combines data frames into single data frame

bins = list(range(0,370,10)) # don't know why this binning works

denom = [0] * len(bins) # init of denominator of ratio (extra particles)

numer = [0] * len(bins) # init of numerator of ratio (neutrons)

angleSet = [0] * len(extraParticles) # init set of angles for entering into data frame

for i in range(len(extraParticles)):
    zPos = extraParticles['z'][i] + 162.5
    xPos = extraParticles['x'][i]
    
    angle = math.atan2(xPos,zPos) * 180 / math.pi

    if xPos < 0:
        angleSet[i] = angle + 360 # necessary for the bottom half of the circle
    else:
        angleSet[i] = angle

extraParticles['angle'] = angleSet

angleSet = [0] * len(data_2112)

for i in range(len(data_2112)):
    zPos = data_2112['z'][i] + 162.5
    xPos = data_2112['x'][i]
    
    angle = math.atan2(xPos,zPos) * 180 / math.pi

    if xPos < 0:
        angleSet[i] = angle + 360
    else:
        angleSet[i] = angle

data_2112['angle'] = angleSet

for i in range(1,37): # counts the number of particles in the given bin
    denom[i-1] = len(extraParticles[extraParticles['angle'] < bins[i]]) - len(extraParticles[extraParticles['angle'] < bins[i-1]])
    numer[i-1] = len(data_2112[data_2112['angle'] < bins[i]]) - len(data_2112[data_2112['angle'] < bins[i-1]])

del denom[-1] # for some reason gives an additional element but I am too afraid to change the range
del numer[-1]

ratio = [0] * 36

for i in range(36):
    ratio[i] = numer[i] / denom[i]

ratioData = pd.DataFrame({'bins':list(range(0,360,10)), 'frequency':ratio})

titleValue = args.file_name

plot = ratioData.plot.bar(x = 'bins', y = 'frequency', position = 0, width = 1, grid = True, title = titleValue, figsize = [10, 10])

fig = plot.get_figure()

fig.savefig(outputIMG)
