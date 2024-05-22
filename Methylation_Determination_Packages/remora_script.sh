#Remora_script##

#! /bin/bash

echo `hostname` 
echo "CUDA: ${CUDA_VISIBLE_DEVICES}" 
echo "SGE: ${SGE_HGR_gpu}" 
if [[ ${SGE_HGR_gpu} == *\ * ]] 
then 
	echo "guppy_basecaller -x 'cuda:${SGE_HGR_gpu// / cuda:}'"
	/cluster/lrcfs/ftiras/bin/ont-guppy_gpu.6.3.8/bin/guppy_basecaller -c dna_r9.4.1_450bps_modbases_5mc_cg_sup.cfg -i /cluster/lrcfs/2397405/projects/nanopore_testing/data/sample/fast5_pass/ -s /cluster/lrcfs/2397405/projects/nanopore_testing/data/sample/basecalledagesampleremoraalignmentv638/ --bam_out -a /cluster/lrcfs/2397405/projects/nanopore_testing/data/sample/wholegenome.fasta --align_type auto --chunk_size 2000 --chunks_per_runner 1024 --gpu_runners_per_device 12 --num_alignment_threads 16 -x "cuda:${SGE_HGR_gpu// / cuda:}" 
else 
	echo "guppy_basecaller -x 'cuda:${SGE_HGR_gpu}'"
	/cluster/lrcfs/ftiras/bin/ont-guppy_gpu.6.3.8/bin/guppy_basecaller -c dna_r9.4.1_450bps_modbases_5mc_cg_sup.cfg -i /cluster/lrcfs/2397405/projects/nanopore_testing/data/sample/fast5_pass/ -s /cluster/lrcfs/2397405/projects/nanopore_testing/data/sample/basecalledagesampleremoraalignmentv638/ --bam_out -a /cluster/lrcfs/2397405/projects/nanopore_testing/data/sample/wholegenome.fasta --align_type auto --chunk_size 2000 --chunks_per_runner 1024 --gpu_runners_per_device 12 --num_alignment_threads 16 -x "cuda:${SGE_HGR_gpu}"
fi
