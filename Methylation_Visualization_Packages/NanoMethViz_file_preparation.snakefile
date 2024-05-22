#Nanomethviz_file_preparation##
rule sortedtext:
	input:
		"per_read_modified_base_calls.txt"
	output:
		"sorted.txt"
	shell:
		"grep ^'read_id' per_read_modified_base_calls.txt > sorted.txt"

rule textgeneration:
	input:
		"per_read_modified_base_calls.txt"
	output:
		"sorted.txt"
	shell:
		"grep -v ^'read_id' per_read_modified_base_calls.txt | sort -k2,2 -k4,4n >> sorted.txt"

rule gunzip:
	input:
		"sorted.txt"
	output:
		"sorted.txt.gz"
	shell:
		"bgzip sorted.txt"
