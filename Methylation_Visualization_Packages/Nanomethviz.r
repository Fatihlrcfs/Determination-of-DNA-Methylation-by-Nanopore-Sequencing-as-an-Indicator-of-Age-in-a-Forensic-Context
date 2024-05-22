#NanoMethViz_R_script#

#Loading Required 
library(NanoMethViz)
library(rtracklayer)
library(dplyr)

#Creating Temporary file
methy_tabix <- file.path  (tempdir(), "methy_data.bgz")

create_tabix_file('sorted.txt.gz', methy_tabix, samples = 'sample_id')

#checking data 
read.table(
  gzfile(methy_tabix), col.names = methy_col_names(), stringsAsFactors = TRUE, nrows = 6)

#importing CRCh38 annotations 
anno <- rtracklayer::import('Homo_sapiens.GRCh38.105.gtf.gz')

#checking CRCh38 annotations
head(anno)

#The ananotations file has a lot more than is required for NanoMethViz which only needs the following columns.
 ##gene_id
 ##chr
 ##strand
 ##start
 ##end
 ##transcript_id
 ##symbol
# Also, chromosome names have to start with ‘chr’, despite the fact that the methylation calls file does not use that nomenclature. It’s a hack, but all chromosomes now prefixed with ‘chr’. Obviously, this will break the unplaced and alternative contig names.

# reformat columns to suit NanoMethViz
anno <- anno %>%
  as.data.frame() %>%
  rename(
    chr = seqnames,
    symbol = gene_name
  ) %>%
  select(gene_id, chr, strand, start, end, transcript_id, symbol)

#checking anno
head(anno)

# create a results object
# the sample name must match above name
nmr = NanoMethResult(methy_tabix,
                     data.frame(
                       sample = 'age56bc10',
                       group = '4'),
                     exons = anno)

# plot a random gene ' ELOVL2'
plot_gene(nmr, 'ELOVL2')
