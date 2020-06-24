#! /usr/bin/env python

import sys
from utils import *

class TE_fams:
  def __init__(self):
    self.fams = []
    self.age = {}
    self.type = {}
    self.len = {}
    self.copy = {}

  def initEntry(self, iD, typ, age, length):
    self.fams.append(iD)
    self.copy[iD] = 1
    self.age[iD] = [age]
    self.len[iD] = [length]
    self.type[iD] = typ

  def addToEntry(self, iD, age, length):
    self.copy[iD] += 1
    self.age[iD].append(age)
    self.len[iD].append(length)

###re-adapted for BED file
    
TE_stats = TE_fams()
genome_len = int(sys.argv[2])

with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    fields = line.split()
    start, stop = int(fields[1]), int(fields[2])
    length = stop - start + 1
    age = fields[-1]#.replace('kimura=', '')
    if age != 'nan':
      age = float(age)
      pre, typ = fields[4], fields[5]
      pre = pre.split('_')
      fam = '_'.join(pre[:-3])
      #if 'LINE' in typ or 'SINE' in typ or 'LTR' in typ or 'DNA' in typ:
      if 'NonLTR' in typ:
        typ = typ.split('/')[1]
      else:
        typ = typ.split('/')[0]
      if fam in TE_stats.fams:
        TE_stats.addToEntry(fam, age, length)
      else:
        TE_stats.initEntry(fam, typ, age, length)

print "#type\tfamily\tinsertions\t%genome\tavg_len\tmed_age\tinsertions-0.05"
for fam in TE_stats.fams:
  young = 0
  for i in TE_stats.age[fam]:
    if i <= 0.05:
      young += 1
  med_age = percentile(sorted(TE_stats.age[fam]), 0.5)
  avg_len = average(TE_stats.len[fam])
  perct_len = float(sum(TE_stats.len[fam]))/genome_len*100
  print "{}\t{}\t{}\t{}\t{}\t{}\t{}".format(TE_stats.type[fam], fam, TE_stats.copy[fam], perct_len, avg_len, med_age, young)
  
  
  

