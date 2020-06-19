#! /usr/bin/env python

import sys
import numpy as np
import math

#piRNAs in sense direction
plus = {}
#piRNAs in anti-sense direction 
minus = {}

#read in bed2 file 
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    fields = line.split()
    ppm, maps = float(fields[-2]), int(fields[-1])

    #store ppm/map count for each + oriented position
    if fields[5] == '+': 
      key = fields[0] + '_' + fields[1] 
      if key in plus:
        plus[key] += ppm/maps
      else:
        plus[key] = ppm/maps
    #do the same for - oriented positions
    else:
      key = fields[0] + '_' + fields[2]
      if key in minus:
        minus[key] += ppm/maps
      else:
        minus[key] = ppm/maps

#keep track of distances between nearby complementary piRNAs 
distances = {}

#read to through + oriented piRNA locations
#i is position index, j is ppm/count 
for i,j in plus.items():
  chrm = i.split('_')[0]
  position = i.split('_')[1]
  position = int(position)
  
  #check - oriented piRNA locations for nearby piRNAs
  #record distance and ppm/count information in distances 
  for k in range(-49,50):
    newPos = position + k
    newKey = chrm + '_' + str(newPos)
    if newKey in minus:
      if k in distances:
        distances[k] += j * minus[newKey]
      else:
        distances[k] = j * minus[newKey]

#performs the inverse from above 
for i, j in minus.items():
  chrm = i.split('_')[0]
  position = i.split('_')[1]
  position = int(position)
  for k in range(-49,50):
    newPos = position - k 
    newKey = chrm + '_' + str(newPos)
    if newKey in plus:
      if k in distances:
        distances[k] += j * plus[newKey]
      else:
        distances[k] = j * plus[newKey]

#calculate Z score for complementary overlaps of 10nt
#background is 1-9 and 11-20

main = 0
background = []
for i in range(1,21):
  if i == 10:
    if i in distances:
      main = distances[i]
    else:
      main = 0
  else:
    if i in distances:
      background.append(distances[i])
    else:
      background.append(0)

#actual Z calculation 
z = (main - np.mean(background))/np.std(background)

#prints the file name prefix of bed2 file and Z score 
if math.isnan(z):
  print "{}\t{}\t{}\t{}".format(sys.argv[1].split('.')[0], 0)
else:
  print "{}\t{}\t{}\t{}".format(sys.argv[1].split('.')[0], z)
