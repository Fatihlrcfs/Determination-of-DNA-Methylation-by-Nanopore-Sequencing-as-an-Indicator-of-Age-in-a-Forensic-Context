#methylartist locus#
#! /bin/bash
#$ -N methylartist_locus
#$ -cwd
#$ -V
#$ -b n
#$ -j y
#$ -pe smp 32
#$ -M 2397405@dundee.ac.uk
#$ -m ae
#$ -cwd
#$ -R y

cat chrxregions.txt | parallel "methylartist locus -i {} -b sample.txt -g Homo_sapiens.GRCh38.106.sorted.gtf.gz --motif CG --ref wholegenome.fasta --smoothwindowsize 10 -p 1,6,1,3,4 --labelgenes --samplepalette viridis --slidingwindowsize 20"
