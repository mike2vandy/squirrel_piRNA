#! /usr/bin/env python

import sys

#input for this script is output of intersectBed (bedtools intersect)
#i.e. intersectBed -a <piRNAs.bed> -b <TEannos.gtf> -wa -wb > <intersect.out>
# the resulting output files will be intersect files for each TE family


with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    fields = line.split('\t')
    TE = fields[16].replace('"', '').replace(';','').split()[1]
    out = open(TE + '.bed','a')
    out.write('\t'.join(fields[:8]) + '\n')
