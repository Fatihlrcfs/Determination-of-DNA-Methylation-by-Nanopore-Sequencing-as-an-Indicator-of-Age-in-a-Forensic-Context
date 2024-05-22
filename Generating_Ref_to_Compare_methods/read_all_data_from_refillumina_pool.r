## Pool data from GSE111631##

# loading libraries
library(minfi)
library(IlluminaHumanMethylationEPICanno.ilm10b4.hg38)
library(IlluminaHumanMethylationEPICanno.ilm10b5.hg38)
library(data.table)
library(stringr)
# path for IDAT file
idatPath <- "GSE111631_RAW" # IDAT dosyalarinin bulundugu klasor
manifestFile <- "GPL21145_MethylationEPIC_15073387_v-1-0.csv" # Manifest dosyasinin adi

# IDAT dosyalarinin tam adlarini listele
idatFiles <- list.files(path = idatPath, pattern = "*.idat", full.names = FALSE)

# Sadece Grn veya Red ile biten dosyalari sec
idatFiles <- idatFiles[grepl("_Grn.idat$|_Red.idat$", idatFiles)]

# Basename olusturmak icin dosya isimlerinden '_Grn.idat' veya '_Red.idat' kisimlarini cikart
basenames <- sub("_Grn.idat$|_Red.idat$", "", idatFiles)

# Benzersiz Basename'leri al (her cift icin bir tane)
basenames <- unique(basenames)

# Hedefler dataframe'ini olustur
targets <- data.frame(Sample_Name = basenames,
                      Sentrix_ID = sub("_(R\\d+C\\d+)$", "", basenames),
                      Sentrix_Position = sub("^.+_(R\\d+C\\d+)$", "\\1", basenames),
                      Basename = basenames,
                      stringsAsFactors = FALSE)

# RGChannelSet nesnesi olustur
rgSet <- read.metharray.exp(base = idatPath, targets = targets)
# RGChannelSet nesnesi olustur, force = TRUE ile
rgSet <- read.metharray.exp(base = idatPath, targets = targets, force = TRUE)

# RGChannelSet nesnesini olusturun
RGset <- read.metharray.exp(base = idatPath, targets = targets, force = TRUE)


#yeni referans ayarlama
RGset@annotation = c(array = "IlluminaHumanMethylationEPIC", annotation = "ilm10b5.hg38")

# on isleme ve normalizasyon adimlari
mSet <- preprocessQuantile(RGset)

# Metilasyon degerlerini hesaplama
betaValues <- getBeta(mSet)

# Koordinatlari ve metilasyon degerlerini iceren bir dataframe olusturma
methylationData <- as.data.frame(betaValues)

# Koordinat bilgilerini ekleyerek genisletilmis dataframe olusturma
coordinates <- getAnnotation(mSet)
extendedData <- cbind(coordinates, methylationData)

# Sonuclari CSV dosyasina yazdirma
outputFile <- "reference_methylation_values.csv"
write.csv(extendedData, file = outputFile, row.names = FALSE)

# islem tamamlandi mesaji
cat("Referans metilasyon dosyasi basariyla olusturuldu: ", outputFile)