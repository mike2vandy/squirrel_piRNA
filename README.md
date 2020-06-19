
# These scripts were used in Vandewege et al. <title> <year>

## normPi.py 
This script will read in a small RNA BED file,  
normalize piRNA count data as parts per million (ppm),  
record how many locations a piRNA mapped to, and create  
a 2nd bed file with the ppm and map count information on each line.  
This script is used prior to calculating Zscores. 
  
Usage:  
`normPi.py <input.bed> > <output.bed2>`  

## piZscore.py
This script calculates 10nt overlap Zscores among overlapping piRNAs for an entire TE family.  
This reads a bed2 file  
  
Usage:  
`piZscore.py <input.bed2> > <Zscore.out>`


