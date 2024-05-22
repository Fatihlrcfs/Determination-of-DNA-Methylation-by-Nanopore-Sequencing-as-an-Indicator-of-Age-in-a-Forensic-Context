#Nanopolish_Snakefile#
sample = ['Sample_Name']

rule all:
	input:
		expand("{sample}_methylation_frequency.tsv", sample=samples)

rule frequency:
	input:
		"{sample}_methylation_calls.tsv"
	output:
		"{sample}_methylation_frequency.tsv"
	shell:
		"python3 /cluster/lrcfs/ccole/github/nanopolish/scripts/calculate_methylation_frequency.py {input} > {output}"

rule index_reads:
	input:
		"{sample}.fastq"
	output:
		"{sample}.fastq.index"
	shell:
		"nanopolish index -d fast5_pass/ {input}"

rule minimap:
	input:
		idx="{sample}.fastq.index",
		reads="{sample}.fastq",
		ref="wholegenome.fasta"
	output:
		bam="{sample}.sorted.bam"
	shell:
		"minimap2 -a -x map-ont {input.ref} {input.reads} | samtools sort -T tmp -o {output}"

rule index_bam:
	input:
		"{sample}.sorted.bam"
	output:
		"{sample}.sorted.bam.bai"
	shell:
		"samtools index {input}"

rule call_meDNA:
	input:
		reads="{sample}.fastq",
		bam="{sample}.sorted.bam",
		bidx="{sample}.sorted.bam.bai"
	output:
		"{sample}_methylation_calls.tsv"
	threads: 8
	shell:
		"nanopolish call-methylation -t {threads} -r {input.reads} -b {input.bam} -g wholegenome.fasta -w '6:8,000,000-13,000,000' > {output}"
