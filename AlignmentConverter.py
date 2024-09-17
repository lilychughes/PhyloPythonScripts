#!/bin/usr/env python

from sys import argv
import argparse
from Bio import AlignIO
from Bio import Seq

parser = argparse.ArgumentParser(description="Requires python 3 and Biopython 1.48 or higher. Use 'phylip-relaxed' if you have taxon names longer than 10 characters or they will be truncated. ")
parser.add_argument('-f', '--file' , dest = 'file' , type = str , default= None , required= True, help = 'Alignment file')
parser.add_argument('-i', '--infmt' , dest = 'infmt', type = str, default= None, required= True, help = 'Input format of alignment file, i.e. fasta, nexus, phylip-relaxed')
parser.add_argument('-o', '--outfmt' , dest = 'outfmt', type = str, default= None, required= True, help = 'Output format of alignment file')
parser.add_argument('-n', '--outfile', dest = 'outfile', type = str, default=None, required= True, help = 'Name of file to write re-formatted alignment to')
args, unknown = parser.parse_known_args()

AlignIO.convert(args.file, args.infmt, args.outfile, args.outfmt, "DNA")
