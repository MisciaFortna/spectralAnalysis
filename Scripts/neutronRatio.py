# @Name: neutronRatio.py
# @Author: Miscia Fortna
# @Date: 28.06.2023
# @Description: script to obtain a histogram of the ratio of neutrons to extra particles at a given degree bin
import argparse
import spectralAnalysis as sp
import pandas as pd
import csv
import math
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description = 'script for neutron to photon+proton ratio') 
parser.add_argument('-n',"--file_name", help = "input csv file (sans filetype)")
parser.add_argument('-p', "--particles", nargs = '+', help = "input extra particles for ratio denominator")
parser.add_argument('-c',"--center", help = "input distance to center of sphere from beam source")
parser.add_argument('-b',"--box", default = 5, help = "input size of box in cm")
parser.add_argument('-d',"--degBins", default = 10, help = "input number of degrees in each bin")
parser.add_argument('-f', "--figsize", nargs = '+', default = [15, 10], help = "input figsize for plot")
args = parser.parse_args()

inputParticles = args.particles

dataLib = sp.reader.read_val(args.file_name)

# particleLib Init
data_temp = data[data['particle']== 2112]
data_temp = data_temp.reset_index()
data_temp.pop('index')

particleLib = {'2112' : data_temp}
# Extra Particles

dataSet = [] # set of data frames for extra particles

for i in inputParticles:
    
    data_temp = dataLib[dataLib['particle']== int(i) ]
    data_temp = data_temp.reset_index()
    data_temp.pop('index')

    particleLib[i] = data_temp

ratioData = sp.sphere.degRatio(particleLib, args.center, box = args.box, degBins = args.degBins)

titleValue = args.file_name

plot = ratioData.plot.bar(x = 'bins', y = 'frequency', position = 0, width = 1, grid = True, title = titleValue, figsize = args.figsize)

fig = plot.get_figure()

outputIMG = args.file_name + "_degRatio.png"

fig.savefig(outputIMG)
