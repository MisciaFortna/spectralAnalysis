# @Name: genReader.py
# @Author: Miscia Fortna
# @Date: 14.06.2023
# @Description: 
#   --txt_2_csv: allows for the input txt file to be converted to a csv file for further analysis
#   --read_val: reads in the input csv file in order to be set into a library of values for the listed particles
#   particle analysis can be left as solely images or the individual sets can be further saved as csv files with "-s"
import argparse
import pandas as pd
import csv
import math
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description = 'script for conversion') 
parser.add_argument('-t',"--txt_2_csv", help = "input file for conversion of particle text files into csv")
parser.add_argument('-r', "--read_val", help = "input file for conversion")
parser.add_argument('-p', "--particles", nargs = '+', help = "input particles to filter for")
parser.add_argument('-s', "--save", action = 'store_true', help = "saves data frames as csv files")
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

if args.read_val:
    input_file = args.read_val + ".csv"
    data = pd.read_csv(input_file, index_col = False)
    dataLib = {}

    for i in args.particles:
        data_temp = data[data['particle']== int(i)]
        data_temp = data_temp.reset_index()
        data_temp.pop('index')
        dataLib[i] = data_temp

    if args.save:
        for i in args.particles:
            output = args.read_val + "_" + i + ".csv"
            dataLib[i].to_csv(output, index = False)

    binList = [0] * 21
    for i in args.particles:
        step = dataLib[i]['energy'].max() / 20
        for j in range(0,21):
            binList[j] = step * j
        plot = dataLib[i].plot.hist(column=['energy'], bins = binList, xticks = binList, xlim = [0, dataLib[i]['energy'].max()], xlabel = 'Energy (MeV)', figsize = [15,10], grid = 1)
        fig = plot.get_figure()
        name = args.read_val + "_" + i + "_hist.png"
        fig.savefig(name)
