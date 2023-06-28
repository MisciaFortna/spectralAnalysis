import argparse
import pandas as pd
import csv
import math
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description = 'script for conversion') 
parser.add_argument('-t',"--txt_2_csv", help = "input file for conversion of particle text files into csv")
parser.add_argument('-r', "--read_val", help = "input file for conversion")
parser.add_argument('-d', "--distance", help = "input distance of shell")
parser.add_argument('-s', "--scatter", action = 'store_true', help = "produces scatter plot for energies")
parser.add_argument('-b', "--histogram", action = 'store_true', help = "produces histogram for degree bins")
args = parser.parse_args()

if args.txt_2_csv:
    input_file = args.txt_2_csv + ".txt"
    output_file = args.txt_2_csv + ".csv"
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

elif args.read_val:

    # Init Files
    input_file = args.read_val + ".csv"

    # Init of Data Set
    data = pd.read_csv(input_file, index_col = False)

    #New For Loop for All Values
    outputSet = [22, 2112, 2212]

    for i in outputSet:
        output_file = args.read_val + "_" + str(i) + ".csv"

        data_temp = data[data['particle']== i]     # Filters for Photons
        data_temp = data_temp[data_temp['y']<=5]   # Filters for y-values below 5 cm
        data_temp = data_temp[data_temp['y']>=-5]  # Filters for y-values above -5 cm

        data_temp.to_csv(output_file, index = False)            # Moves Photon Data to Output to Reset Array Values
        data_temp = pd.read_csv(output_file, index_col = False) # Rereads Chart

        position = data_temp.shape # Sets 2-Value Array of Shape

        rows = position[0]       # Sets Row Value as Data_22 Row Total

        angleSet = [0] * rows    # Init Angle Set as Zeroes in Shape of Row

        for j in range(rows):
            zPos = data_temp['z'][j] + 162.5
            xPos = data_temp['x'][j]
            angle = math.atan2(xPos, zPos) * 180 / math.pi
            if xPos < 0:
                angleSet[j] = angle + 360
            else:
                angleSet[j] = angle

        data_temp['angle'] = angleSet
        data_temp.to_csv(output_file, index = False)            # Moves Photon Data to Output to Reset Array Values
        data_temp = pd.read_csv(output_file, index_col = False) # Rereads Chart
        titleValue = 'Particle ' + str(i) + ' at r = ' + args.distance + ' cm'
        if args.scatter:
            plot = data_temp.plot(kind = 'scatter', x = 'angle', y = 'energy', xticks = range(0, 380, 20), title = titleValue, xlabel = 'Degrees from Beamline', ylabel = 'Energy (MeV)', figsize = [10,10])
            fig = plot.get_figure()
            name = args.read_val + "_" + str(i) + "_scatter.png"
            fig.savefig(name)
        if args.histogram:
            binList = list(range(0,370,10))
            plot = data_temp.plot.hist(column=["angle"], bins = binList, xticks = range(0, 370, 10), xlim = [0, 360], title = titleValue, xlabel = 'Degrees from Beamline', figsize = [15,10], grid = 1)
            fig = plot.get_figure()
            name = args.read_val + "_" + str(i) + "_hist.png"
            fig.savefig(name)

