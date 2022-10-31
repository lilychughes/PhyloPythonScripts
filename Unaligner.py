#!/usr/bin/env python3

import re
from sys import argv
import argparse

import Bio
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


parser = argparse.ArgumentParser(description="Requires python 3 and Biopython. Removes gaps from aligned sequences in FASTA format.")
parser.add_argument('-f', '--fasta' , dest = 'fasta' , type = str , default= None , required= True, help = 'FASTA alignment')
parser.add_argument('-o', '--output', dest = 'output', type = str, default = None, required = True, help = 'Name of output file')
args, unknown = parser.parse_known_args()

alignment = open(args.fasta)

records = list(SeqIO.parse(alignment, "fasta"))

unaligned = []

for record in records:
    clean_seq = record.seq.replace("-","")
    clean_rec = SeqRecord(id=record.id, seq=clean_seq, description='')
    unaligned.append(clean_rec)
    
SeqIO.write(unaligned, args.output, "fasta")