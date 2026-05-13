input <- "bioinfor/annovar/humandb/hg38_refGeneWithVerMrna.fa"

headers <- readLines(input, warn = FALSE)
headers <- headers[startsWith(headers, ">")]

chr <- sub(".*leftmost exon at (chr[0-9XY]+)[:_].*", "\\1", headers)
chr <- chr[grepl("^chr([1-9]|1[0-9]|2[0-2]|X|Y)$", chr)]

counts <- as.data.frame(table(chr), stringsAsFactors = FALSE)
names(counts) <- c("chromosome", "rna_sequence_count")
counts$chr_order <- match(counts$chromosome, c(paste0("chr", 1:22), "chrX", "chrY"))
counts <- counts[order(counts$chr_order), c("chromosome", "rna_sequence_count")]

lengths <- data.frame(
  chromosome = paste0("chr", 1:22),
  length_bp = c(
    248956422, 242193529, 198295559, 190214555, 181538259, 170805979,
    159345973, 145138636, 138394717, 133797422, 135086622, 133275309,
    114364328, 107043718, 101991189, 90338345, 83257441, 80373285,
    58617616, 64444167, 46709983, 50818468
  )
)

autosomes <- merge(counts, lengths, by = "chromosome")
autosomes$chr_num <- as.integer(sub("chr", "", autosomes$chromosome))
autosomes <- autosomes[order(autosomes$chr_num), ]
autosomes$length_mb <- autosomes$length_bp / 1e6
autosomes$rna_per_mb <- autosomes$rna_sequence_count / autosomes$length_mb
autosomes <- autosomes[, c("chromosome", "length_bp", "length_mb", "rna_sequence_count", "rna_per_mb")]

write.csv(counts, "report/chr_sequence_counts_all.csv", row.names = FALSE)
write.csv(autosomes, "report/chr_sequence_counts_autosomes.csv", row.names = FALSE)

cor_value <- cor(autosomes$length_mb, autosomes$rna_sequence_count)
sink("report/correlation_summary.txt")
cat(sprintf("Pearson correlation between autosome length and RNA sequence count: %.3f\n", cor_value))
cat(sprintf("chr21 RNA sequence count: %d\n", counts$rna_sequence_count[counts$chromosome == "chr21"]))
sink()

png("report/chr_length_vs_rna_count.png", width = 1800, height = 1200, res = 180)
par(mar = c(5, 5, 3, 1))
plot(
  autosomes$length_mb,
  autosomes$rna_sequence_count,
  pch = 19,
  col = "#2F6F73",
  xlab = "Chromosome length (Mb)",
  ylab = "RNA sequence count",
  main = "RNA sequence count vs. chromosome length (autosomes)"
)
text(
  autosomes$length_mb,
  autosomes$rna_sequence_count,
  labels = autosomes$chromosome,
  pos = 3,
  cex = 0.72,
  col = "#333333"
)
fit <- lm(rna_sequence_count ~ length_mb, data = autosomes)
abline(fit, col = "#C55A11", lwd = 2)
legend(
  "topleft",
  legend = sprintf("Pearson r = %.3f", cor_value),
  bty = "n",
  text.col = "#333333"
)
dev.off()

png("report/chr_rna_counts_barplot.png", width = 1800, height = 1000, res = 180)
par(mar = c(5, 5, 3, 1))
barplot(
  counts$rna_sequence_count,
  names.arg = counts$chromosome,
  col = "#7FA8A9",
  border = NA,
  las = 2,
  ylab = "RNA sequence count",
  main = "RNA sequence count by chromosome"
)
dev.off()
