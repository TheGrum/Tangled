#!/usr/bin/python

"""
detangler.py - Copyright (c) 2012, Howard C. Shaw III
Licensed under the GNU GPL v3

detangler.py [filename] ...

Pass any number of filenames, detangler will extract all trees using BioPython,
and optimize them all simultaneously, minimizing on all combinations of trees.
"""

from sys import argv
from Bio import Phylo
from detangle import tree, node
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser(description = 'Minimize tangling across multiple trees.')
    parser.add_argument('-t, --output-type', default='nexus', choices=['newick', 'nexus', 'phyloxml'])
    parser.add_argument('-o, --output-filename', nargs='?')
    parser.add_argument('infiles', nargs='+')
    args = parser.parse_args()

    bio_trees = {}
    bio_tree_list = []
    for filename in args.infiles:
        """ Work out what format the file is, then parse the trees out """
        f = open(filename, 'r')
        first = f.readline()
        if first.find('nexus') > -1:
            tree_type='nexus'
        elif first.find('<') > -1:
            tree_type='phyloxml'
        else:
            tree_type='newick'
        f.close()
        print filename, tree_type
        temp = list(Phylo.parse(filename,tree_type))
        for i in temp:
            bio_trees[i.name] = i
            bio_tree_list.append(i)
    trees = {}
    tree_list = {}
    """ At this point, bio_trees is full, now we need to convert these Phylo trees to the detangle
    trees which are optimized for rotations. """
    for i in bio_tree_list:
        tr = tree()
        tr.init_from_phylo(i)
        trees[tr.name]=tr
        tree_list.append(tr)