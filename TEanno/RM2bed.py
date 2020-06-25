#! /usr/bin/python

import sys

#Meant to read in a TE consensus file
#ie. RepeatMasker/Libraries/RepeatMasker.lib to compare a hit length against the consensus length
seq_dict = {}
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    if line.startswith('>'):
      header = line.split()[0].replace('>', '')
      seq_dict[header] = ''
    else:
      seq_dict[header] += line


#Reads the output of calcDivergenceFromAlignModified.pl as an input file
#outputs tab delimited version of the same file  
with open(sys.argv[2]) as f:
  for line in f:
    line = line.strip()
    fields = line.split()
    chrom, start, end = fields[4], int(fields[5]), int(fields[6])
    length = end - start
    orient = fields[8].replace('C', '-')
    element_id = fields[9].split('#')[0]
    element_type = fields[9].split('#')[1]
    try: 
      cons_len = len(seq_dict[element_id + '#' + element_type])
      perct = float(length) / float(cons_len) * 100
      k2p = fields[len(fields)-1].replace('kimura=', '')
      print "{0}\t{1}\t{2}\t{3}\t{4}_{0}_{1}_{2}\t{5}\t{6}\t{7}".format(chrom, start, end, orient, element_id, element_type, perct, k2p)
    except:
      pass
f.close()

