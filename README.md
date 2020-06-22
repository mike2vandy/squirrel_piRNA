
# These scripts were used in Vandewege et al. <title> <year>

## normPi.py 
This script will read in a small RNA BED file,  
normalize piRNA count data as parts per million (ppm),  
record how many locations a piRNA mapped to, and create  
a 2nd bed file with the ppm and map count information on each line.  
This script is used prior to calculating Zscores. 
  
Usage:  
`normPi.py <input.bed> > <output.bed2>`  

## splitIntersect.py  
After intersecting mapped small RNAs and TE annotatios, I use this script to  
split the intersect file into individual TE family files. 

Usage: 
`splitIntersect.py <intersectBed.out>`  

## piZscore.py
This script calculates 10nt overlap Zscores among overlapping piRNAs for an entire TE family.  
This reads a bed2 file  
  
Usage:  
`piZscore.py <input.bed2> > <Zscore.out>`

## Overall pipeline pseudocode  

bamToBed -i <mappedPirna.bam> > <mappedPirna.bed>

normPi.py <mappedPirna.bed> > <mappedPirna.bed2>

intersectBed -a <mappedPirna.bed2> -b <TEannos.gtf> -wa -wb > <piTEintersect.out>

splitIntersect.py <piTEintersect.out>

for i in TEfamilyIntersects; do piZscrore.py $i; done


