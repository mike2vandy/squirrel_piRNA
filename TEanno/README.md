
# These scripts were used in Vandewege et al. <title> <year>

# Overall pipeline pseudocode to work with TE annotations

calcDivergenceFromAlignModified.pl <RepeatMaskerOutput.align> > <k2p.out>

RM2bed.py <consensusSequences.fas> <k2p.out> > <k2p.bed>

sortBed -i <k2p.bed> |clusterBed -s > <k2p.clustered.bed>

filterTEAnnos.py <k2p.clustered.bed> > <k2p.filtered.bed>

statsForTEFamilies.py <k2p.filtered.bed> <genomeSize[int]> > <TEStats.out>

bed2gtf.py <k2p.filtered.bed> > <k2p.filtered.gtf>

## calcDivergenceFromAlignModified.pl  

This script is a modification of a Perl script that comes with RepeatMasker. It will read a .align file and produce a tab delimited TE annotation file with Kimura 2-parameter distances.  

This is was modified from an older version of calcDivervgence and RepeatMasker has since updated. However, this script will work on modern .align output files if placed in a RepeatMasker/utils directory.  

Usage:  
`calcDivergenceFromAlignModified.pl <RepeatMaskerOutput.align> > <k2p.out>`  

## RM2bed.py  

Converts the calcDivergenceFromAlign output into a .bed file. Has a column for the percent length of the hit compared to the consensus sequence and had to read in a fasta file of consensus sequences.  

Usage:  
`RM2bed.py <consensusSequences.fas> <k2p.out> > <k2p.bed>`  

## filterTEAnnos.py  

Attempts to pick the best TE annotation when there are overlapping annotations.  

Running the raw bed file through clusterBed (bedtools cluster) is required first:  

`sortBed -i <k2p.bed> |clusterBed -s > <k2p.clustered.bed>`

Usage:  
`filterTEAnnos.py <k2p.clustered.bed> > <k2p.filtered.bed>`  

## statsForTEFamilies.py

Will calculate properties of individual TE families that include the number of insertions, the percent of the genome made up of those insertions, the average insertion length, the median k2p divergence, and number of young insertions, k2p < 0.05. Produces a tab-delimeted file. It does require a manual input of the genome size.  

Usage:  
`statsForTEFamilies.py <k2p.filtered.bed> <genomeSize[int]> > <TEStats.out>`  

## bed2gtf.py  

Produces a specific gtf file required for TEtranscripts from the custom made bed file.  

Usage:  
`bed2gtf.py <k2p.filtered.bed> > <k2p.filtered.gtf>`
