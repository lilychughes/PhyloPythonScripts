#!/usr/bin/env python3

import re
from sys import argv
import argparse
import os


parser = argparse.ArgumentParser(description="script notes")
parser.add_argument('-i', '--input' , dest = 'input' , type = str , default= None , required= True, help = 'Blast results in table format (-outfmt 6 with blast command line).')
parser.add_argument('-o', '--output', dest = 'output', type = str, default = None, required = True, help = 'Name of output file.')
parser.add_argument('-p', '--pident', dest = 'pident', type = float, default = 99.9, required = False, help = 'Minimum percent identity from blast results to flag. Default 99.9')
parser.add_argument('-c', '--coverage', dest = 'coverage', type = float, default = 50, required = False, help = 'Minimum query coverage (qcovs) from blast results to flag. Default 50')
parser.add_argument('-l', '--length', dest = 'length', type = float, default = 100, required = False, help = 'Minimum alignment length to flag. Default 100')
parser.add_argument('-f', '--family', dest = 'family', type = str, default = 'False', required = False, help = 'Set to True if you do not want to flag sequences from the same family that are above the identity threshold. Assumes sequences are named with the following format: Family_Genus_species')
parser.add_argument('-g', '--genus', dest = 'genus', type = str, default = 'False', required = False, help = 'Set to True if you do not want to flag sequences from the same genus that are above the identity threshold. Assumes sequences are named with the following format: Family_Genus_species')
parser.add_argument('-d', '--drop', dest = 'drop', type = str, default = 'False', required = False, help = 'Set to True if you want to print a list of taxon names to drop to a file. You can feed this file to the DropTaxa.py script with the FASTA file to remove these sequences.')
args, unknown = parser.parse_known_args()



# open the input blast file
inp = open(args.input)

# the order of columns in the blast output are: qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue qcovs
# this is a customization of the -outfmt 6 option in blast+, which does not by default print query coverage (qcovs)


# make an empty list to store 
check = []

for line in inp:
    liner = line.split("\t")
    qseqid = liner[0]
    sseqid = liner[1]
    pident = float(liner[2])
    length = float(liner[3])
    qcovs = float(liner[11])
    qfamily = qseqid.split("_")[0]
    qgenus = qseqid.split("_")[1]
    sfamily = sseqid.split("_")[0]
    sgenus = sseqid.split("_")[1]
    if qseqid not in sseqid:
        if pident > args.pident and qcovs > args.coverage and length > args.length:
            if 'False' in args.family and 'False' in args.genus:
                check.append(line)
            elif 'True' in args.family and 'False' in args.genus:
                if qfamily not in sfamily:
                    check.append(line)
            elif 'True' in args.family and 'True' in args.genus:
                if qfamily not in sfamily:
                    if qgenus not in sgenus:
                        check.append(line)
            elif 'False' in args.family and 'True' in args.genus:
                if qgenus not in sgenus:
                    check.append(line)

inp.close()

# Check flagged sequences for reciprocity
reciprocal = []

combos = []

for line in check:
    liner = line.split("\t")
    qseqid = liner[0]
    sseqid = liner[1]
    combos.append(qseqid+"\t"+sseqid)

for line in check:
    liner = line.split("\t")
    qseqid = liner[0]
    sseqid = liner[1]
    if sseqid+"\t"+qseqid in combos:
        reciprocal.append(line)

if len(reciprocal) > 0:
    out = open(args.output, "w")
    for line in reciprocal:
        out.write(line)
    out.close()
else:
    print("All sequences passed filters in "+args.input)
    

if 'True' in args.drop and len(reciprocal) > 0:
    names = []
    for line in reciprocal:
        liner = line.split("\t")
        qseqid = liner[0]
        sseqid = liner[1]
        if qseqid not in names:
            names.append(qseqid)
        if sseqid not in names:
            names.append(sseqid)
    drop = open(args.output+".drop", "w")
    for item in names:
        drop.write(item+"\n")
    drop.close()