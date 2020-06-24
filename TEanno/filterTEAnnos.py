#! /usr/bin/env python

import sys
from collections import OrderedDict, Callable

#Attempts to chose the best TE annotation for overlapping annotations

#Copied class, maintains an ordered dictionary 
class DefaultOrderedDict(OrderedDict):
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and not callable(default_factory)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))
    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory, OrderedDict.__repr__(self))


#other functions
def average(l):
  return sum(l)/len(l)

def printFields(j):
  print '\t'.join(map(str, j[:-1]))


#attempts to pick the best overlapping annotation given K2P distance to consensus and length of the annotation
#aiming for the most complete annotation with the lowest K2P 
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
  
  #optimal annotation, was both the most complete and had the lowest K2P
  for i in j:
    if i[6] == highestPct and i[7] == lowestK2P:
      theBest = i

  if theBest:
    return theBest
  
  #compares changes in TE annotations, rarest scenario 
  #if there were 2 overlapping LINE annotations and there isn't a clear winner
  #compare differences in k2p and pct length of consensus
  #i.e. TE1_k2p = 0.05 and TE2_k2p = 0.07, k2pDiff = 0.05/0.07 = 0.7
  #and TE1_pct = 80 and TE2_pct = 40, pctDiff = 40/80 0.5
  #since there was a bigger change in TEpct, I would select the more complete (TE1) as the 
  #best annotation
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
    
    try:
      pctDiff = pcts[1]/pcts[0]
    except:
      pctDiff = 0

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
  #examines how much annotations overlap
  #if greater than 25% overlapping, same region is getting annotated  
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
    #if less than 25% overlap, assume annotations are not overlappping
    else:
      for i in j:
	if i[1] == starts[count] and i[2] == ends[count]:
	  if i not in nons:
	    nons.append(i)
	elif i[1] == starts[count + 1] and i[2] == ends[count + 1]:
	  if i not in nons:
	    nons.append(i)
    
    count += 1
  
  #if "nonoverlapping", return annotations 
  for i in nons:
    if i not in overlaps:
      allSorted.append(i)

  #otherwise select best of overlapping 
  if overlaps:
    likely = pickBest(overlaps)
    allSorted.append(likely)  
  
  allSorted.sort(key = lambda x: x[1])
  
  return allSorted

#finds the start and stop of the simple repeat, returns 1 annotation
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

#2nd major function
def checkCluster(j):
  #check if TE types in cluster are same, i.e. LINE and LTR
  types = []
  for i in j:
    if i[5] not in types:
      types.append(i[5])
  #if only 1 TE type and its a simple repeat, print it
  if len(types) == 1:
    if types[0] == 'Simple':
      simple = filterSimple(j)
      printFields(simple)
    #if 1 TE type and not simple, select best
    else:
      mostLikely = checkOverlap(j)
      for i in mostLikely:
        printFields(i)
  #if 2 or more TE types in annotation cluster 
  else:
    bestICanDo = checkOverlap(j)
    for i in bestICanDo:
      printFields(i)
    
###MAIN###

#Reads in bed file produced by RM2bed.py and clusterBed 
#Going to save all the hits for each cluster of annotations 
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
      cluster = fields[-1] #cluster number produced by clusterBed
      if cluster in data:
        data[cluster].append(fields)
      else:
        data[cluster] = [fields]

#look through each cluster, if only 1 annotation (most common), 
#print that annotation otherwise select "best" annotation
for i, j in data.items():
  if len(j) == 1:
    printFields(j[0])
  else:
    checkCluster(j)

