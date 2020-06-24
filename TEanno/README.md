
# These scripts were used in Vandewege et al. <title> <year>

## calcDivergenceFromAlignModified.pl  

This script is a modification of a Perl script that comes with RepeatMasker. It will read a .align file and produce a tab delimited TE annotation file with Kimura 2-parameter distances.  

This is was modified from an older version of calcDivervgence and RepeatMasker has since updated. However, this script will work on modern .align output files if placed in a RepeatMasker/utils directory.  

Usage:  
`calcDivergenceFromAlignModified.pl <RepeatMaskerOutput.align> > <k2p.out>`  

## RM2bed.py  

Converts the calcDivergenceFromAlign output into a .bed file. Has a column for the percent length of the hit compared to the consensus sequence and had to read in a fasta file of consensus sequences.  

Usage:  
`RM2bed.py <consensusSequences.fas> <k2p.out> > <k2p.bed>`  

## 

