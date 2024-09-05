#!/usr/bin/env python3

import re
from sys import argv
import argparse

import glob

from Bio.Nexus import Nexus
from Bio import AlignIO

###### Documentation

parser = argparse.ArgumentParser(description="Concatenates nexus-formatted alignment files with a minimum number of sequences. Requires biopython. Adapted from: https://biopython.org/wiki/Concatenate_nexus")
parser.add_argument('-e', '--ext', dest = 'ext', type = str, default=".nex", required= False, help = 'File extension of NEXUS formatted alignment files. Default is .nex')
parser.add_argument('-m', '--minimum', dest = 'minimum', type = int, default= 1, required= True, help = 'Minimum number of sequences per alignment to include in concatenated file. Default is 1 and will concatenate all alignments.')
parser.add_argument('-o', '--output', dest = 'output', type = str, default= "SuperMatrix.nex", required= True, help = 'Name of output file. Default is SuperMatrix.nex')

args, unknown = parser.parse_known_args()

######

# Get a list of nexus alignment files
file_list = glob.glob("*"+args.ext)
file_list.sort()

# Make a list of alignments that have the minimum number of sequences (user-defined) to concatenate
min_files = []

for file in file_list:
    a = AlignIO.read(file, format = "nexus")
    if len(a) >= args.minimum:
        min_files.append(file)

# Make a list of tuples for Nexus.combine function

nexi = [(fname, Nexus.Nexus(fname)) for fname in min_files]

combined = Nexus.combine(nexi)
combined.write_nexus_data(filename=open(args.output, "w"))