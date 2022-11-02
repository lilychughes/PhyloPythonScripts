#!/usr/bin/env python3

import re
from sys import argv
import argparse

import glob

import Bio
from Bio import AlignIO


###### Documentation

parser = argparse.ArgumentParser(description="Requires python3 & Biopython 1.75 or greater. Writes RAxML-style partition files with three codon positions. Output ends in .part")
parser.add_argument('-a', '--alignments' , dest = 'alignments' , type = str , default= None , required= True, help = 'Directory with FASTA alignments.')
parser.add_argument('-e', '--ext', dest = 'ext', type = str, default=".fasta", required= False, help = 'File extension of FASTA formatted alignment files. Default is .fasta')

args, unknown = parser.parse_known_args()

#######

# Make a list of alignments to process
alignments = []

for a in glob.glob(args.alignments+"*"+args.ext):
    alignments.append(a)


# Write partition files & flag alignments not divisible by 3

for a in alignments:
    ali = AlignIO.read(a, "fasta")
    seqlen = len(ali[0])
    if seqlen % 3 == 0:
        strlen = str(seqlen)
        p1 = "DNA, p1 = 1-" + strlen + "\\3" + "\n"
        p2 = "DNA, p2 = 2-" + strlen + "\\3" + "\n"
        p3 = "DNA, p3 = 3-" + strlen + "\\3" + "\n"
        output = open(a+".part", "w")
        output.write(p1 + p2 + p3)
        output.close()
    else:
        print(a+" is not divisible by 3. Please check codon positions.")    