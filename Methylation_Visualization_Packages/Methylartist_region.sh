#Methylartist_region#
#! /bin/bash
#$ -N methylartist_script
#$ -cwd
#$ -V
#$ -b n
#$ -j y
#$ -pe smp 32
#$ -M 2397405@dundee.ac.uk 
#$ -m ae 
#$ -cwd
#$ -R y

cat chrX.txt | parallel "methylartist region -i {} -b sample.txt -p 32 -g Homo_sapiens.GRCh38.106.sorted.gtf.gz -n CG -r wholegenome.fasta --maxuncovered 100 --smoothwindowsize 10 --skip_align_plot --panelratios 1,0,1,4 --height 6.5 --genepalette viridis --samplepalette viridis"
