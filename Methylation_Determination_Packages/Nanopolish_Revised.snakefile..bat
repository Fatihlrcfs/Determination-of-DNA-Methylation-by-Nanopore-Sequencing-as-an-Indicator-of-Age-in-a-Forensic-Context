## Revised Nanopolish Snakefile ##
sample = ['Sample_name']

rule all:
	input:
		expand("{sample}_methylation_frequency.tsv", sample=sample)


rule index:
    input:
        f5="fast5_pass/",
        fq="{sample}.fastq"
    output:
        "{sample}.fastq.index",
        "{sample}.fastq.index.fai",
        "{sample}.fastq.index.gzi",
        "{sample}.fastq.index.readdb"
    shell:
        "nanopolish index -d {input.f5} {input.fq}"

rule minimap2: # snakemake wrappers for minimap2
    input:
        target="wholegenome.fasta", # can be either genome index or genome fasta
        query=["{sample}.fastq"]
    output:
        "nanopolish_results2/mapped/{sample}.bam"
    log:
        "nanopolish_results2/mapped/{sample}.log"
    params:
        extra="-a -x map-ont"
    threads: 6
    wrapper:
        "v1.5.0/bio/minimap2/aligner"

rule samtools_sort:
    input:
        "nanopolish_results2/mapped/{sample}.bam"
    output:
        "nanopolish_results2/mapped/{sample}.sorted.bam"
    shell:
        "samtools sort -o {output} {input}"

rule samtools_index:
    input:
        "nanopolish_results2/mapped/{sample}.sorted.bam"
    output:
        "nanopolish_results2/mapped/{sample}.sorted.bam.bai"
    shell:
        "samtools index {input}"

rule call_methylation:
    input:
        bam="nanopolish_results2/mapped/{sample}.sorted.bam",
        bai="nanopolish_results2/mapped/{sample}.sorted.bam.bai",
        fa="wholegenome.fasta",
        fq="{sample}.fastq",
        index="{sample}.fastq.index",
        fai="{sample}.fastq.index.fai",
        gzi="{sample}.fastq.index.gzi",
        readdb="{sample}.fastq.index.readdb"
    output:
        "nanopolish_results2/{sample}_nanopolish-log.tsv"
    shell:
        "nanopolish call-methylation -t 10 -r {input.fq} -b {input.bam} -g {input.fa} --progress > {output}"

rule split_cpgs:
    input:
        "nanopolish_results2/{sample}_nanopolish-log.tsv"
    output:
        "nanopolish_results2/{sample}_nanopolish-log-perCG.tsv"
    script:
        "script_in_snakemake/split_cpg_groups.py"

rule calculate_frequency:
    input:
        script="script_in_snakemake/run_nanopolish.R",
        log="nanopolish_results2/{sample}_nanopolish-log-perCG.tsv"
    output:
        file1="nanopolish_results2/{sample}_nanopolish-freq-perCG.tsv",
        file2="nanopolish_results2/{sample}_nanopolish-freq-perCG-combStrand.tsv"
    shell:
        "Rscript {input.script} {input.log} {output.file1} {output.file2}"
