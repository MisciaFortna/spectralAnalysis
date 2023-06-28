# @Name: sphere.py
# @Author: Miscia Fortna
# @Date: 28.06.2023
# @Description: module for sphere-related functions
#   - degRatio : returns dataframe of ratio between neutrons and other particles
#       @Inputs:
#           * dataLib: Dictionary of Particle Dataframes
#           * box: Height of Dosimeter Box for Flux in cm
#           * degBins: Number of Degree Bins
#           * center: The Center Position Along Beam Line
#       @Outputs: Dataframe of Ratio Data
#       @Notes:
#           * Assumed that beam is along z axis positive to negative
#           * 0 Degrees is towards beamline
import pandas as pd
import csv
import math
import matplotlib.pyplot as plt

def degRatio(dataLib, center, **kwargs):
    defaultKwargs = { 'degBins': 10, 'box' : 5 }
    kwargs = { **defaultKwargs, **kwargs }
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
