#!/usr/bin/env python3

import re
from sys import argv
import argparse

from ete3 import Tree,TreeNode
import glob

###### Documentation

parser = argparse.ArgumentParser(description="Requires python 3 and the python package ete3. Collapses branches in a tree under a user-defined support threshold. This script was written by Lily Hughes, lilychughes@gmail.com. ")
parser.add_argument('-d', '--directory' , dest = 'directory' , type = str , default= None , required= True, help = 'Directory with newick-formatted gene trees.')
parser.add_argument('-e', '--ext' , dest = 'ext' , type = str , default= ".treefile" , required= False, help = 'File extension of gene trees. Default .treefile')
parser.add_argument('-b', '--bootstrap' , dest = 'bootstrap' , type = int , default= 33 , required= False, help = 'Minimum bootstrap support value to maintain a branch. Branches below this value will be collapsed. Default value = 33.')

args, unknown = parser.parse_known_args()
#######

# Make a list of alignments to process
trees = []

for a in glob.glob(args.directory+"*"+args.ext):
    trees.append(a)

for tree in trees:
    t = Tree(tree)
# Collapse nodes with less than args.cutoff bootstrap support
    for node in t.traverse():
        if not node.is_leaf() and not node.is_root():
            if node.support < args.bootstrap :
                node.delete()
# Write the output
    t.write(outfile=tree+".collapsed."+str(args.bootstrap)+".tre")              

