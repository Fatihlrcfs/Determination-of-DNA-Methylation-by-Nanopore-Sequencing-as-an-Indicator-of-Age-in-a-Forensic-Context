#methylartist_sorting#
rule tabix_sortedsamtools:
	input:
		"Homo_sapiens.GRCh38.106.gtf.gz"
	output:
		"Homo_sapiens.GRCh38.106.sorted.gtf.gz"
	shell:
		"(grep ^"#" Homo_sapiens.GRCh38.106.gtf.gz; grep -v ^"#" Homo_sapiens.GRCh38.106.gtf.gz | sort -k1,1 -k4,4n) | bgzip > Homo_sapiens.GRCh38.106.sorted.gtf.gz"
