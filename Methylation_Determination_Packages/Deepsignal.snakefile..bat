# Deepsignal_Snakefile#
samples = ['samplesingle']

rule all:
	input:
		expand("{sample}_deepsignal-freq-perCG-combStrand.tsv", sample=samples)

rule combine_sites:
    input:
        freq="{sample}_fast5s.CG.call_mods.frequency.tsv",
        script="script_in_snakemake/run_deepsignal.R"
    output:
        file1="{sample}_deepsignal-freq-perCG.tsv",
        file2="{sample}_deepsignal-freq-perCG-combStrand.tsv"
    shell:
        "Rscript {input.script} {input.freq} {output.file1} {output.file2}"

rule create_input_for_comb_model:
    input:
        prob="{sample}_fast5s.CG.call_mods.tsv",
        script="script_in_snakemake/format_deepsignal.R"
    output:
        "{sample}_deepsignal-perRead-score.tsv"
    shell:
        "Rscript {input.script} {input.prob} {output}"
