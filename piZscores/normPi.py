#! /usr/bin/env python

import sys

"""
this script will read a bedfile twice
once to count piRNA mapped position 
the 2nd to append count information

this is a preliminary step to normalize 
read and map count information for use in Zscore calculation
"""

#keep count of piRNA counts 
piCounts = {}

#keep count of positions piRNA mapped to
piMaps = {}

#read standard bedfile from bamToBed 
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    fields = line.split()
    piRNA = fields[3]
    count = piRNA.split('-')[1]
    count = int(count)
    if piRNA not in piCounts:
      piCounts[piRNA] = count
    if piRNA in piMaps:
      piMaps[piRNA] += 1
    else:
      piMaps[piRNA] = 1

#to normalize piRNAs as parts per million 
total = sum(piCounts.values())

#read bedfile 2nd time and output count and ppm information 
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    fields = line.split()
    piRNA = fields[3]
    count = piRNA.split('-')[1]
    count = float(count)
    ppm = count/total * 1000000
    print "{}\t{}\t{}".format(line, str(round(ppm, 4)), piMaps[piRNA])
