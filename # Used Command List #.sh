# Used Command List #
## Basecalling ##
###  Basecalling Command ###
qsub -pe smp 56 -jc 4week -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y /cluster/lrcfs/ftiras/bin/ont-guppy-cpu-5.0.16/bin/guppy_basecaller -c dna_r9.4.1_450bps_modbases_5mc_hac.cfg -i fast5_pass/ -s basecalled/ --num_callers 2 --cpu_threads_per_caller 28 
## Quality Control ##
### NanoPlot Job Submission with 'sequencing_summary.file' ###
qsub -pe smp 5  -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y NanoPlot --summary sequencing_summary.txt --loglength --N50 --tsv_stats  -o summary-plots-log-transformed
### NanoPlot Job Submission with 'fastq.file' ###
qsub -pe smp 8 -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y NanoPlot -t 8 –fastq file.fastq --maxlength 40000 --plots dot --legacy hex -o fastq_summary-plots-log-transformed
## Methylation Determination Packages ##
### NAnopolish ###
#### Nanopolish Snakefile Submission ####
snakemake -j 2 Snakefile --cores all --cluster "qsub -V -cwd -pe smp 20 -jc 4week -M 2397405@dundee.ac.uk -m abe" --latency-wait 60
###Deepsignal##
#### Deepsignal Single fast5  Generation with 'ont_fast5_api'####
qsub -pe smp 30 -jc long -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y multi_to_single_fast5 -i samplefast5/ -s sample_multitosinglefast5/ -t 30 --recursive
#### Deepsignal Job Submission ####
qsub -adds l_hard gpu 4 -adds l_hard cuda.0.name 'NVIDIA A40' -pe smp 30 -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y /cluster/lrcfs/ftiras/bin/ont-guppy_gpu.6.2.1/bin/guppy_basecaller -c dna_r9.4.1_450bps_hac.cfg -i sample_multitosinglefast5/ -r -s basecalledsamplehacdeepsignal2/ --chunk_size 2000 --chunks_per_runner 1024 --gpu_runners_per_device 15 -x 'auto'
#### Deepsignal Tombo Preprocess  ####
qsub -pe smp 20 -jc 4week -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y tombo preprocess annotate_raw_with_fastqs --fast5-basedir samplemultitosinglefast5/ --fastq-filenames sample_single.fastq --sequencing-summary-filenames deepsignal2basecalledhacsamplesinglefast5/sequencing_summary.txt --basecall-group Basecall_1D_000 --basecall-subgroup BaseCalled_template --overwrite --processes 20
#### Deepsignal Hdf5 Plugin ####
export HDF5_PLUGIN_PATH=/cluster/lrcfs/2397405/bin/ont-vbz-hdf-plugin-1.0.1-Linux/usr/local/hdf5/lib/plugin
#### Deepsignal Tombo Resquigle ####
qsub -pe smp 20 -jc 4week -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y tombo resquiggle samplesinglefast5/ wholegenome.fasta --ignore-read-locks --processes 20 --corrected-group RawGenomeCorrected_000 --basecall-group Basecall_1D_000 --overwrite
#### Deepsignal Extract ####
qsub -pe smp 30 -jc 4week -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y deepsignal2 extract -i samplemultitosinglefast5/ -o sample_fast5s.CG.features.tsv --corrected_group RawGenomeCorrected_000 --nproc 30 --motifs CG
#### Deepsignal Call ####
qsub -adds l_hard gpu 2 -pe smp 30 -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y deepsignal2 call_mods --input_path sample_fast5s.CG.features.tsv --model_path model.dp2.CG.R9.4_1D.human_hx1_t2t.both_bilstm.b17_s16_epoch7.ckpt --result_file sample_fast5s.CG.call_mods.tsv --nproc 30
#### Deepsignal Methylation Call ####
qsub -pe smp 10 -jc long -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y python /cluster/lrcfs/2397405/bin/deepsignal2downloaded/deepsignal2files/scripts/call_modification_frequency.py --input_path sample_fast5s.CG.call_mods.tsv --result_file sample_fast5s.CG.call_mods.frequency.tsv
### Megalodon ###
#### Megalodon Basecalling ####
qsub -adds l_hard gpu 4 -adds l_hard cuda.0.name 'NVIDIA A40' -pe smp 32 -jc long -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y megalodon fast5_pass/ --outputs basecalls mappings mod_mappings per_read_mods mods --reference wholegenome.fasta --write-mods-text --processes 32 --guppy-server-path /cluster/lrcfs/2397405/bin/ont-guppy_gpu.6.1.1/bin/guppy_basecall_server --guppy-config dna_r9.4.1_450bps_hac.cfg --remora-modified-bases dna_r9.4.1_e8 hac 0.0.0 5mc CG 0 --mod-motif m CG 0 --overwrite --devices "cuda:all" --output-directory megalodon_result_sample
### Remora ###
#### Remora Scrit Submission ####
qsub -jc long -adds l_hard gpu 4 -adds l_hard cuda.0.name 'NVIDIA A40' -pe smp 32  -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y bash remora_script.sh
#### Remora Combining and Sorting ####
echo "samtools cat basecalledsampleremoraalignmentv638/pass/*.bam | samtools sort -o sampleoutput.sorted_mapped.bam" | qsub -pe smp 20 -M 2397405@dundee.ac.uk -m ae -cwd
#### Remora Modbam2bed ####
modbam2bed --aggregate --prefix 5mC_per_genomic_position_agg -m 5mC -e --cpg -t 8 -a 0.2 -b 0.8 wholegenome.fasta remorav638sortedmappedbam/sample.sorted2_mapped.bam > 5mC_per_genomic_position_sample.bed
## Methylation Visualization ##
###Methyplotlib###
qsub -pe smp 5  -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y methplotlib -m sample_methylation_calls.tsv sample_methylation_frequency.tsv -n elovl2samplefrequency -w 6:10,980,759-11,045,000 -g gencode.v39.annotation.gtf.gz --simplify -b sample.sorted.bed
###Methylartist###
#### Generating database from methylation packages####
methylartist db-nanopolish -m sample_call-methylation.tsv.gz -d sample.nanopolish.db 
#### Generating segment; .txt file include sorted.bam and .db file####
methylartist segmeth -d data_nanopolish.txt -i genes_locations.bed -p 32
####generating violin plot, Here, the segment output produced in the previous step is used as input####
methylartist segplot -s 5genes_locations_nanopolish.tsv -v 
#### Methylartist region Script Submission ####
qsub -adds l_hard gpu 1 -pe smp 32 -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y sh  ./Methylartist_region.sh 
#### Methylartist locus Script Submission ####
qsub -adds l_hard gpu 1 -pe smp 32 -M 2397405@dundee.ac.uk -m ae -cwd -b y -R y sh  ./Methylartist_locus.sh 
