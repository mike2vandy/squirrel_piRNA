#! /usr/bin/env python

import sys
from utils import *

def average(l):
  return sum(l)/len(l)

def printFields(j):
  print '\t'.join(map(str, j[:-1]))

def pickBest(j):
  
  highestPct = 0
  lowestK2P = 2
  theBest = []
  
  for i in j:
    pct, k2p = i[6], i[7]
    if pct > highestPct:
      highestPct = pct
    if k2p < lowestK2P:
      lowestK2P = k2p
      
  for i in j:
    if i[6] == highestPct and i[7] == lowestK2P:
      theBest = i

  if theBest:
    return theBest
  
  else:
    k2ps = []
    pcts = []
    for i in j:
      k2ps.append(i[7])
      pcts.append(i[6])
    k2ps.sort()
    pcts.sort(reverse = True)
    
    try:
      k2pDiff = k2ps[0]/k2ps[1]
    except:
      k2pDiff = 0
    
    #try:
    pctDiff = pcts[1]/pcts[0]
    #except:
    #  pctDiff = 0

    if k2pDiff < pctDiff:
      good = k2ps[0]
      for i in j:
	if float(i[7]) == good:
	  return i
    else:
      good = pcts[0]
      for i in j:
	if float(i[6]) == good:
	  return i
    
  
def checkOverlap(j):
  starts = []
  ends = []
  for i in j:
    starts.append(i[1])
    ends.append(i[2])

  overlaps = []
  nons = []
  allSorted = []
  
  count = 0
  while count <= len(starts) - 2:
    length = ends[count] - starts[count]
    overlap = ends[count] - starts[count + 1]
    pctOver = float(overlap) / length
      
    if pctOver >= 0.25:
      for i in j:
	if i[1] == starts[count] and i[2] == ends[count]:
	  if i not in overlaps:
	    overlaps.append(i)
	if i[1] == starts[count + 1] and i[2] == ends[count + 1]:
	  if i not in overlaps:
	    overlaps.append(i)
    else:
      for i in j:
	if i[1] == starts[count] and i[2] == ends[count]:
	  if i not in nons:
	    nons.append(i)
	elif i[1] == starts[count + 1] and i[2] == ends[count + 1]:
	  if i not in nons:
	    nons.append(i)
    
    count += 1
  
  for i in nons:
    if i not in overlaps:
      allSorted.append(i)

  if overlaps:
    likely = pickBest(overlaps)
    allSorted.append(likely)  
  
  allSorted.sort(key = lambda x: x[1])
  
  return allSorted
  
def filterSimple(j):
  pct = []
  k2p = []
  clus = j[0][-1]
  chrm, start, stop, = j[0][0], j[0][1], j[-1][2]
  orient = j[0][3]
  typ = j[0][4].split('_')[0]
  kind = j[0][5]
  for i in j:
    pct.append(i[6])
    k2p.append(i[7])
  oPct, oK2P = average(pct), average(k2p)
  merged = [chrm, start, stop, orient, typ, kind, oPct, oK2P, clus]
  return merged

#2nd major function, prints here    
def checkCluster(j):
  types = []
  for i in j:
    if i[5] not in types:
      types.append(i[5])
  if len(types) == 1:
    if types[0] == 'Simple':
      simple = filterSimple(j)
      printFields(simple)
    else:
      mostLikely = checkOverlap(j)
      for i in mostLikely:
        printFields(i)
  else:
    bestICanDo = checkOverlap(j)
    for i in bestICanDo:
      printFields(i)
    
###MAIN###

#Reads in a tab delimited repeat masker k2p file

data = DefaultOrderedDict()
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    fields = line.split()
    #start and stop positions
    fields[1], fields[2] = int(fields[1]), int(fields[2])
    if fields[2] - fields[1] == 0:
      pass
    else:
      fields[6], fields[7] = float(fields[6]), float(fields[7])
      cluster = fields[-1]
      if cluster in data:
        data[cluster].append(fields)
      else:
        data[cluster] = [fields]

for i, j in data.items():
  if len(j) == 1:
    printFields(j[0])
  else:
    checkCluster(j)

