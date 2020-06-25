#! /usr/bin/env python2.7

import sys

transCount = {}
with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    fields = line.split()
    chrm, start, stop, orient = fields[0:4]
    typ0, TEtemp = fields[4], fields[5].split('/')
    typ = typ0.split('_')
    transId = '-'.join(typ[0:-3])
    geneId = transId
    RNA = False
    if len(TEtemp) == 1:
      if 'RNA' in TEtemp[0]:
        RNA = True
        pass
      else:
        classId, familyId = TEtemp[0].replace('?', ''), transId 
    else:
      classId, familyId = TEtemp[0], TEtemp[1] 
    if RNA == False:
      if transId in transCount:
        transCount[transId] += 1
        print "{}\trmsk\texon\t{}\t{}\t.\t{}\t.\tgene_id \"{}\"; transcript_id \"{}_dup{}\"; family_id \"{}\"; class_id \"{}\";".format(chrm, start, stop, orient, geneId, transId, transCount[transId], familyId, classId)
      else:
        transCount[transId] = 0
        print "{}\trmsk\texon\t{}\t{}\t.\t{}\t.\tgene_id \"{}\"; transcript_id \"{}\"; family_id \"{}\"; class_id \"{}\";".format(chrm, start, stop, orient, geneId, transId, familyId, classId)
    
   
