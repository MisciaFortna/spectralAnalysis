# @Name: genReader.py
# @Author: Miscia Fortna
# @Date: 14.06.2023
# @Description: 
#   --txt_2_csv: allows for the input txt file to be converted to a csv file for further analysis
#   --read_val: reads in the input csv file in order to be set into a library of values for the listed particles
#   particle analysis can be left as solely images or the individual sets can be further saved as csv files with "-s"
import argparse
import spectralAnalysis as sp
import pandas as pd
import csv
import math
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description = 'script for conversion') 
parser.add_argument('-T',"--txt_2_csv", help = "input file for conversion of particle text files into csv")
parser.add_argument('-P',"--phsp_2_csv", help = "input file for conversion of particle phsp files into csv")
parser.add_argument('-r', "--read_val", help = "input file for particle reading")
parser.add_argument('-p', "--particles", nargs = '+', help = "input particles to filter for")
parser.add_argument('-s', "--save", action = 'store_true', help = "saves data frames as csv files")
parser.add_argument('-d', "--display", action = 'store_true', help = "saves data frames as csv files")
args = parser.parse_args()

if args.txt_2_csv:
    sp.reader.txt_2_csv(args.txt_2_csv)

if args.phsp_2_csv:
    sp.reader.phsp_2_csv(args.phsp_2_csv)

if args.read_val:
    if args.save and args.display:
        dataLib = sp.reader.read_val(args.read_val, save = 1)
        particles = list(dataLib.keys())
        for i in particles:
            fName = args.read_val + "_" + i
            fig = sp.splotting.ePlot(fName, i)
            name = args.read_val + "_" + i + "_hist.png"
            fig.savefig(name)
    elif args.save:
        sp.reader.save_val(args.read_val)
    else:
        print("Error 1: Incorrect Inputs") 
