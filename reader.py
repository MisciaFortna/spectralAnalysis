# @Name: reader.py
# @Author: Miscia Fortna
# @Date: 15.06.2023
# @Description: Library of Spectral Reading Functions from Previous Scripts
#   - phsp_2_csv: converts phsp file to csv (Needs header file otherwise gives default 10 columns)
#       @Inputs: fName: File Name (sans file type)
#       @Outputs: A Saved CSV File
#   - txt_2_csv: converts txt file to csv (NB txt file MUST BE COMMA DELIM AT BEGINNING OF LINES)(Needs header file otherwise gives default 10 columns)
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
#   - save_val: redundant save function
#       @Inputs:
#           * fName: File Name of CSV (sans file type)
#           * kwargs: 
#               -- particles: Str List of Particle ID Numbers
#       @Outputs:
#           * Collection of Particle-Filtered CSV Files
import pandas as pd
import csv
import math
import matplotlib.pyplot as plt
import re
from tempfile import NamedTemporaryFile
from shutil import move

# Private Function
def colGen(fName):
    column_names = []
    default_columns = ['empty','x','y','z','cos(x)','cos(y)','energy','weight','particle','neg_cos(z)','first_particle']
    iFile = fName + ".header"
    try:
       test = open(iFile, 'r')
    except OSError:
        return default_columns
    else:
        test.close()
        with open(iFile, 'r') as file:
            for line in file:
                match = re.match(r'\s*(\d+): (.+)', line)
                if match:
                    l_no = int(match.group(1))
                    if l_no >= 11:
                        print(match.group(1))
                        column_name = match.group(2).strip()
                        column_names.append(column_name)

        full_col_names = default_columns + column_names
        return full_col_names

def phsp_2_csv(fName):

    input_file = fName + ".phsp"
    input_header = fName + ".header"
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
                full_names = colGen(input_header)
                writer.writerow(full_names)
                #writer.writerow(('empty','x','y','z','cos(x)','cos(y)','energy','weight','particle','neg_cos(z)','first_particle'))
                writer.writerows(lines)
    edit_output = pd.read_csv(output_file, index_col = False)
    edit_output.pop('empty')
    edit_output.to_csv(output_file, index = False)

def txt_2_csv(fName):
    input_file = fName + ".txt"
    input_header = fName + ".header"
    output_file = fName + ".csv"
    with open(input_file, 'r') as infile:
        stripped = (line.strip() for line in infile)
        lines = (line.split(",") for line in stripped if line)
        with open(output_file, 'w') as outfile:
            writer = csv.writer(outfile)
            full_names = colGen(input_header)
            writer.writerow(full_names)
            #writer.writerow(('empty','x','y','z','cos(x)','cos(y)','energy','weight','particle','neg_cos(z)','first_particle'))
            writer.writerows(lines)
    edit_output = pd.read_csv(output_file, index_col = False)
    edit_output.pop('empty')
    edit_output.to_csv(output_file, index = False)

# b1 save
# vf4 particles
def read_val(fName,**kwargs):
    defaultKwargs = { 'save': False, 'particles': ['default']} # particles called 'default' just as an unexpected value for the condition
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
    return dataLib

# vf4 particles
def save_val(fname, **kwargs): # redundant save function
    defaultKwargs = { 'particles': ['default']} # particles called 'default' just as an unexpected value for the condition
    kwargs = { **defaultKwargs, **kwargs }
    input_file = fName + ".csv"
    data = pd.read_csv(input_file, index_col = False)
    if kwargs['particles'] == ['default']:
        particles = data['particle'].unique().tolist()
        for i in range(len(particles)):
            particles[i] = str(particles[i])
    else:
        particles = kwargs['particles']

    for i in particles:
        data_temp = data[data['particle']== int(i)]
        data_temp = data_temp.reset_index()
        data_temp.pop('index')
        output = fName + "_" + i + ".csv"
        data_temp.to_csv(output, index = False)
