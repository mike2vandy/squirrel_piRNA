#! /usr/bin/env python

import sys
from math import ceil, floor

#class to hold count information
#records the number of insertions, length, #k2p distance
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

#average from a list
def average(N):
    return sum(N)/float(len(N))

#Calculate a given percentile from a sorted array
def percentile(N, percent, key=lambda x:x):
    k = (len(N)-1) * percent
    f = floor(k)
    c = ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1

## MAIN ##

TE_stats = TE_fams()

#To calculate genome percent, requires manual input of the genome size
genome_len = int(sys.argv[2])

#Filtered bed file 
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    fields = line.split()
    start, stop = int(fields[1]), int(fields[2])
    length = stop - start + 1 #insertion length
    age = fields[-1] #K2P
    if age != 'nan':
      age = float(age)
      pre, typ = fields[4], fields[5]
      pre = pre.split('_')
      #specific family and location is given it's own locus
      fam = '_'.join(pre[:-3])
      if '/' in typ: 
        typ = typ.split('/')[0]
      if fam in TE_stats.fams:
        TE_stats.addToEntry(fam, age, length)
      else:
        TE_stats.initEntry(fam, typ, age, length)

#For each TE family, output the number of insertions, % of the genome
#average insertion length, median k2p, and #insertions with k2p < 0.05
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
  
  
  

