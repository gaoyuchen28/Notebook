#!/usr/bin/env Rscript

# 关闭包加载时的提示信息，避免终端输出太乱。
# 这里加载了 7 个包：
# 1. data.table：更高效地处理表格数据
# 2. rpart：训练决策树模型
# 3. ggplot2：画图
# 4. dplyr：更方便做表连接和筛选
# 5. tibble：把一些“隐藏信息”转成普通列
# 6. clusterProfiler：提供 bitr()，用于基因 ID 转换
# 7. org.Hs.eg.db：人类基因注释数据库
suppressPackageStartupMessages({
  library(data.table)
  library(rpart)
  library(ggplot2)
  library(dplyr)
  library(tibble)
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

# 固定随机种子。
# 这样“随机抽样”每次都会得到同样的结果，方便复现和交作业。
set.seed(20260403)

# 下面 3 行是在定义输出文件夹路径。
# 我们把所有结果统一放到 tcga_hw_outputs 里，
# 图片放到 figures 子文件夹，表格放到 tables 子文件夹。
out_dir <- "tcga_hw_outputs"
fig_dir <- file.path(out_dir, "figures")
tab_dir <- file.path(out_dir, "tables")

# 创建文件夹。
# showWarnings = FALSE 表示如果文件夹已经存在，就不要报无关紧要的警告。
# recursive = TRUE 表示如果上级目录不存在，就一起创建。
dir.create(out_dir, showWarnings = FALSE)
dir.create(fig_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(tab_dir, showWarnings = FALSE, recursive = TRUE)

# 这是一个“手写 AUC”的函数。
# AUC 是 ROC 曲线下面积，用来衡量一个二分类模型把正类和负类分开的能力。
# 这里：
# labels01 必须是 0/1 标签，1 表示 Tumor，0 表示 Normal
# scores 是模型给出的“越大越像 Tumor”的分数
auc_manual <- function(labels01, scores) {
  # 正类样本个数，也就是 Tumor 的数量
  n_pos <- sum(labels01 == 1)

  # 负类样本个数，也就是 Normal 的数量
  n_neg <- sum(labels01 == 0)

  # 对模型分数做排序名次。
  # 分数越高，说明模型越相信它是 Tumor。
  ranks <- rank(scores)

  # 这是 Mann-Whitney U 的等价写法，可以计算 AUC。
  # 如果 AUC 接近 1，说明模型区分 Tumor/Normal 的能力强。
  (sum(ranks[labels01 == 1]) - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)
}

# 这个函数用于生成 ROC 曲线上的点。
# ROC 曲线本质上是在不同阈值下，统计：
# 1. TPR（真正率 / 召回率）
# 2. FPR（假正率）
roc_points <- function(labels01, scores) {
  # 按分数从高到低排序。
  # 因为 ROC 曲线的思想是：从“最像 Tumor”的样本开始逐步往下放宽阈值。
  ord <- order(scores, decreasing = TRUE)

  # 把标签按相同顺序重排。
  labels_sorted <- labels01[ord]

  # 把分数也按相同顺序重排。
  scores_sorted <- scores[ord]

  # 统计总共有多少个正类（Tumor）。
  pos_total <- sum(labels_sorted == 1)

  # 统计总共有多少个负类（Normal）。
  neg_total <- sum(labels_sorted == 0)

  # cumsum 是累积求和。
  # 当我们从高分样本往低分样本逐个放进“预测为 Tumor”的集合时，
  # tp 表示到当前阈值为止抓到了多少个真正的 Tumor。
  tp <- cumsum(labels_sorted == 1)

  # fp 表示到当前阈值为止误抓了多少个 Normal。
  fp <- cumsum(labels_sorted == 0)

  # 用 data.table 存储每个阈值对应的 ROC 点。
  dt <- data.table(
    threshold = scores_sorted,
    tpr = tp / pos_total,
    fpr = fp / neg_total
  )

  # 给 ROC 曲线补上起点 (0,0) 和终点 (1,1)。
  # unique 是为了避免重复点。
  unique(rbind(
    data.table(threshold = Inf, tpr = 0, fpr = 0),
    dt,
    data.table(threshold = -Inf, tpr = 1, fpr = 1)
  ))
}

# 这个函数负责汇总模型评价指标。
# 输入：
# 1. actual：真实类别
# 2. predicted：模型预测类别
# 3. tumor_prob：模型给出的“是 Tumor 的概率/分数”
metric_summary <- function(actual, predicted, tumor_prob) {
  # 混淆矩阵。
  # 行表示真实类别，列表示预测类别。
  cm <- table(actual, predicted)

  # 下面 4 个量是二分类里最基本的概念：
  # tn：真实是 Normal，预测也是 Normal
  tn <- cm["Normal", "Normal"]

  # fp：真实是 Normal，但预测成了 Tumor
  fp <- cm["Normal", "Tumor"]

  # fn：真实是 Tumor，但预测成了 Normal
  fn <- cm["Tumor", "Normal"]

  # tp：真实是 Tumor，预测也是 Tumor
  tp <- cm["Tumor", "Tumor"]

  # Accuracy：整体正确率
  accuracy <- (tp + tn) / sum(cm)

  # Precision：模型判成 Tumor 的样本里，有多少是真的 Tumor
  precision <- tp / (tp + fp)

  # Recall：所有真实 Tumor 里，有多少被成功抓到
  recall <- tp / (tp + fn)

  # Specificity：所有真实 Normal 里，有多少被正确识别为 Normal
  specificity <- tn / (tn + fp)

  # F1：Precision 和 Recall 的综合指标
  f1 <- 2 * precision * recall / (precision + recall)

  # AUC：用前面自己写的函数计算
  auc <- auc_manual(ifelse(actual == "Tumor", 1, 0), tumor_prob)

  # 返回一个列表，里面有两部分：
  # 1. confusion：混淆矩阵表
  # 2. overall：总体评价指标
  list(
    confusion = as.data.table(cm, keep.rownames = "Actual"),
    overall = data.table(
      Accuracy = accuracy,
      Precision = precision,
      Recall = recall,
      Specificity = specificity,
      F1 = f1,
      AUC = auc
    )
  )
}

# 在终端打印当前步骤，方便知道程序执行到哪里了。
message("Loading TCGA LIHC expression matrix...")

# 读取压缩的 tsv 文件。
# gzfile() 负责打开 .gz 压缩文件，
# read.delim() 把它读成一个表格。
# check.names = FALSE 表示保留原始列名，不自动改列名。
raw_df <- read.delim(gzfile("TCGA-LIHC.star_counts (2).tsv.gz"), check.names = FALSE)

# 第一列是 Ensembl 基因 ID，像 ENSG00000123456.7。
# 这里把点号后面的版本号去掉，只保留主 ID，后面更方便展示。
ensembl_id <- sub("\\..*$", "", raw_df[[1]])

# 取出除了第一列之外的所有列名，也就是样本 ID。
sample_ids <- colnames(raw_df)[-1]

# TCGA barcode 的第 14-15 位代表样本类型。
# 例如：
# 01 常常表示 Tumor
# 11 常常表示 Normal
# 所以这里截取第 14-15 位作为样本类型编码。
sample_type_code <- substr(sample_ids, 14, 15)

# 把所有样本先整理成一张表，方便后面统计。
sample_type_all <- data.table(
  Sample = sample_ids,
  SampleTypeCode = sample_type_code,
  Group = fifelse(sample_type_code == "01", "Tumor",
                  fifelse(sample_type_code == "11", "Normal", "Other"))
)

# 保存每个样本的原始分组信息。
fwrite(sample_type_all, file.path(tab_dir, "sample_type_all.csv"))

# 按样本类型编码和分组做数量统计，并保存。
fwrite(
  sample_type_all[, .N, by = .(SampleTypeCode, Group)][order(Group, SampleTypeCode)],
  file.path(tab_dir, "sample_type_counts_all.csv")
)

# 这里只保留真正要做分类的样本：
# 01 = Tumor
# 11 = Normal
# 其他样本类型先不参与这次作业。
keep_idx <- sample_type_code %in% c("01", "11")

# 更新样本 ID，只保留 Tumor/Normal。
sample_ids <- sample_ids[keep_idx]

# 为每个样本创建类别标签。
# factor 表示分类变量。
# levels = c("Normal", "Tumor") 是在明确类别顺序。
labels <- factor(
  ifelse(sample_type_code[keep_idx] == "01", "Tumor", "Normal"),
  levels = c("Normal", "Tumor")
)

# 提取表达矩阵：
# raw_df[, -1] 表示去掉第一列基因 ID，只保留数值表达量
# 再用 keep_idx 保留 Tumor/Normal 的样本列
# as.matrix() 把表格转换成矩阵，后面做数值计算更方便。
expr_mat <- as.matrix(raw_df[, -1, drop = FALSE])[, keep_idx, drop = FALSE]

# 给矩阵的每一行加上基因名。
rownames(expr_mat) <- ensembl_id

# 到这里为止，我们手里只有 Ensembl ID，例如 ENSG00000123456。
# 但老师看报告时，通常更希望看到常见的基因名（gene symbol），例如 TP53、ALB。
# 所以下面补一个“基因 ID 转换”步骤。

# 先把所有用到的 Ensembl ID 去重，整理成一列。
gene_id_table <- data.frame(
  ENSEMBL_clean = unique(ensembl_id),
  stringsAsFactors = FALSE
)

# 用 bitr() 做 ID 转换。
# 含义如下：
# 1. 输入 ID 类型是 ENSEMBL
# 2. 输出希望得到 SYMBOL
# 3. 使用人类注释数据库 org.Hs.eg.db
# 4. drop = FALSE 表示即使有些基因没有匹配到，也先保留，后面自己处理
gene_map <- bitr(
  gene_id_table$ENSEMBL_clean,
  fromType = "ENSEMBL",
  toType = "SYMBOL",
  OrgDb = org.Hs.eg.db,
  drop = FALSE
)

# 为了和后面自己构造的字段名保持一致，
# 这里把 bitr() 返回结果中的 ENSEMBL 列改名为 ENSEMBL_clean。
colnames(gene_map)[colnames(gene_map) == "ENSEMBL"] <- "ENSEMBL_clean"

# 保存完整的 ID 转换表。
fwrite(as.data.table(gene_map), file.path(tab_dir, "ensembl_to_symbol_map.csv"))

# 建立一张“样本与类别”的对应表。
sample_info <- data.table(
  Sample = sample_ids,
  Class = labels
)

# 保存用于分析的样本明细表。
fwrite(sample_info, file.path(tab_dir, "sample_info_used.csv"))

# 保存 Tumor 和 Normal 的样本数量统计表。
fwrite(sample_info[, .N, by = Class], file.path(tab_dir, "sample_counts_used.csv"))

# 提示开始划分训练集和测试集。
message("Creating stratified train/test split...")

# 这是“分层抽样”的关键代码。
# 作用：让 Tumor 和 Normal 各自按 70% 进入训练集。
# 这样做比完全随机更稳，因为可以保证两类在训练集里都存在。
train_idx <- unlist(
  tapply(seq_along(labels), labels, function(i) sample(i, ceiling(length(i) * 0.7)))
)

# 测试集就是剩下没被抽进训练集的样本。
test_idx <- setdiff(seq_along(labels), train_idx)

# 取出训练集和测试集的样本信息。
train_info <- sample_info[train_idx]
test_info <- sample_info[test_idx]

# 保存训练集类别数量。
fwrite(train_info[, .N, by = Class], file.path(tab_dir, "train_class_counts.csv"))

# 保存测试集类别数量。
fwrite(test_info[, .N, by = Class], file.path(tab_dir, "test_class_counts.csv"))

# 从表达矩阵中切出训练集样本列。
train_expr <- expr_mat[, train_idx, drop = FALSE]

# 从表达矩阵中切出测试集样本列。
test_expr <- expr_mat[, test_idx, drop = FALSE]

# 取出训练集标签。
train_labels <- labels[train_idx]

# 取出测试集标签。
test_labels <- labels[test_idx]

# 提示开始做特征选择。
message("Selecting Top50 differential genes from the training set...")

# 下面这一步是在做“差异表达筛选”。
# 我们只在训练集里筛基因，避免提前偷看测试集信息。

# 计算每个基因在 Tumor 训练样本中的平均表达量。
tumor_mean <- rowMeans(train_expr[, train_labels == "Tumor", drop = FALSE])

# 计算每个基因在 Normal 训练样本中的平均表达量。
normal_mean <- rowMeans(train_expr[, train_labels == "Normal", drop = FALSE])

# LogFC 在这里直接用“肿瘤均值 - 正常均值”来表示差异方向和大小。
# 值越大，表示 Tumor 更高；值越小，表示 Normal 更高。
log_fc <- tumor_mean - normal_mean

# 对每个基因做一次 t 检验，比较 Tumor 和 Normal 的表达是否有显著差异。
# apply(train_expr, 1, ...) 表示对每一行（每个基因）重复做这件事。
p_value <- apply(train_expr, 1, function(v) {
  tryCatch(
    t.test(v[train_labels == "Tumor"], v[train_labels == "Normal"])$p.value,
    error = function(e) 1
  )
})

# BH 校正：因为这里一次性检验了很多基因，所以要做多重检验校正。
# padj 越小，说明这个基因的差异越可信。
padj <- p.adjust(p_value, method = "BH")

# 整理成一张差异表达结果表。
de_table <- data.table(
  Gene = rownames(train_expr),
  MeanTumor = tumor_mean,
  MeanNormal = normal_mean,
  LogFC = log_fc,
  PValue = p_value,
  Padj = padj
)

# 额外增加一列绝对差异大小，方便排序。
de_table[, AbsLogFC := abs(LogFC)]

# 去掉无效结果，比如 p 值不是正常数字的情况。
de_table <- de_table[is.finite(PValue) & !is.na(Padj)]

# 排序规则：
# 1. 先按 Padj 从小到大
# 2. 如果 Padj 接近，再按 |LogFC| 从大到小
setorder(de_table, Padj, -AbsLogFC)

# 给差异表达结果补上基因 Symbol。
# 这里参考你给的那段代码思路：
# 先整理出 ENSEMBL_clean，再和 gene_map 做表连接。
de_table_with_symbol <- as.data.frame(de_table) %>%
  mutate(ENSEMBL_clean = Gene) %>%
  left_join(gene_map, by = "ENSEMBL_clean")

# 保存完整的训练集差异表达结果。
fwrite(de_table, file.path(tab_dir, "differential_expression_training_all.csv"))
fwrite(as.data.table(de_table_with_symbol), file.path(tab_dir, "differential_expression_training_all_with_symbol.csv"))

# 取前 50 个差异最显著的基因，作为模型输入特征。
top50_genes <- de_table$Gene[1:50]

# 单独保存前 50 基因表。
top50_table <- de_table[1:50]

# 单独保存前 10 基因表，方便报告里展示。
top10_table <- de_table[1:10]

# 给 Top50 和 Top10 表也补上 Symbol。
top50_table_with_symbol <- as.data.frame(top50_table) %>%
  mutate(ENSEMBL_clean = Gene) %>%
  left_join(gene_map, by = "ENSEMBL_clean")

top10_table_with_symbol <- as.data.frame(top10_table) %>%
  mutate(ENSEMBL_clean = Gene) %>%
  left_join(gene_map, by = "ENSEMBL_clean")

fwrite(top50_table, file.path(tab_dir, "top50_differential_genes.csv"))
fwrite(top10_table, file.path(tab_dir, "top10_differential_genes.csv"))
fwrite(as.data.table(top50_table_with_symbol), file.path(tab_dir, "top50_differential_genes_with_symbol.csv"))
fwrite(as.data.table(top10_table_with_symbol), file.path(tab_dir, "top10_differential_genes_with_symbol.csv"))

# 这里为 Top50 建立“特征名称映射表”。
# 目的不是改变基因本身，而是让后面的图和决策树结构更容易读懂：
# 1. 有基因 Symbol 时优先显示 Symbol
# 2. 没有 Symbol 时回退到 Ensembl ID
# 3. 如果同一个 Symbol 重复出现，make.unique() 会自动补后缀，避免列名重复
feature_map <- as.data.table(top50_table_with_symbol)[
  ,
  .(Gene, SYMBOL)
]
feature_map[, DisplayGene := ifelse(!is.na(SYMBOL) & SYMBOL != "", SYMBOL, Gene)]
feature_map[, DisplayGene := make.unique(DisplayGene)]
fwrite(feature_map, file.path(tab_dir, "top50_feature_display_map.csv"))

# 提示开始准备机器学习模型输入格式。
message("Preparing model matrices...")

# 机器学习模型通常要求：
# 1. 每一行是一个样本
# 2. 每一列是一个特征
# 但原始表达矩阵是“每一行一个基因，每一列一个样本”，所以需要转置。
train_df <- data.frame(
  Class = train_labels,
  t(train_expr[top50_genes, , drop = FALSE]),
  check.names = FALSE
)

# 把模型特征列改成“基因名优先”的展示名称。
# 这样：
# 1. 决策树结构图中的分裂条件更直观
# 2. 后面的变量重要性图也能直接显示基因名称
colnames(train_df)[-1] <- feature_map$DisplayGene

# 用同样的方法准备测试集。
test_df <- data.frame(
  Class = test_labels,
  t(test_expr[top50_genes, , drop = FALSE]),
  check.names = FALSE
)

# 测试集列名必须和训练集完全一致，否则 predict() 时会找不到对应特征。
colnames(test_df)[-1] <- feature_map$DisplayGene

# 提示开始训练决策树模型。
message("Training decision tree classifier...")

# 训练决策树。
# Class ~ . 的意思是：
# 用除了 Class 之外的所有列，去预测 Class。
tree_model <- rpart(
  Class ~ .,
  data = train_df,
  method = "class",

  # 这里手动把两类先验概率都设成 0.5，
  # 目的是减少类别不平衡对模型的影响。
  parms = list(prior = c(0.5, 0.5)),

  # 决策树控制参数：
  # cp：分裂阈值，越小树越容易继续长
  # maxdepth：树最大深度
  # minbucket：每个叶节点最少样本数
  control = rpart.control(cp = 0.001, maxdepth = 5, minbucket = 4)
)

# 用训练好的决策树对测试集做“类别预测”。
tree_pred <- predict(tree_model, newdata = test_df, type = "class")

# 同时输出 Tumor 概率，后面算 ROC/AUC 要用。
tree_prob <- predict(tree_model, newdata = test_df, type = "prob")[, "Tumor"]

# 汇总测试集上的评价指标。
metrics <- metric_summary(test_df$Class, tree_pred, tree_prob)

# 保存总体指标表。
fwrite(metrics$overall, file.path(tab_dir, "decision_tree_metrics.csv"))

# 保存混淆矩阵。
fwrite(metrics$confusion, file.path(tab_dir, "decision_tree_confusion_matrix.csv"))

# 提取决策树的变量重要性。
# 这里的重要性可以粗略理解成：
# 某个基因对模型做判断到底有多重要。
tree_importance <- data.table(
  Gene = names(tree_model$variable.importance),
  Importance = as.numeric(tree_model$variable.importance)
)

# 按重要性从高到低排序。
setorder(tree_importance, -Importance)

# 保存变量重要性表。
fwrite(tree_importance, file.path(tab_dir, "decision_tree_variable_importance.csv"))

# 当前的 tree_importance$Gene 已经是“展示名称”了。
# 所以这里再把它和 feature_map 对回来，补上原始 Ensembl 和 Symbol。
tree_importance_with_symbol <- as.data.frame(tree_importance) %>%
  left_join(as.data.frame(feature_map), by = c("Gene" = "DisplayGene"))

fwrite(as.data.table(tree_importance_with_symbol), file.path(tab_dir, "decision_tree_variable_importance_with_symbol.csv"))

# 保存测试集每个样本的预测详情。
prediction_table <- data.table(
  Sample = test_info$Sample,
  Actual = test_df$Class,
  Predicted = tree_pred,
  TumorProbability = tree_prob
)
fwrite(prediction_table, file.path(tab_dir, "test_predictions.csv"))

# 生成 ROC 曲线坐标点并保存。
roc_df <- roc_points(ifelse(test_df$Class == "Tumor", 1, 0), tree_prob)
fwrite(roc_df, file.path(tab_dir, "decision_tree_roc_points.csv"))

# 提示开始画图。
message("Generating figures...")

# 为了画图，先复制前 10 差异基因表。
top20_plot <- as.data.table(top10_table_with_symbol)

# 为了让图更好读，这里额外生成一个“展示名称”：
# 1. 如果有基因 Symbol，就优先显示 Symbol
# 2. 如果没有 Symbol，就退回显示 Ensembl ID
top20_plot[, DisplayGene := ifelse(!is.na(SYMBOL) & SYMBOL != "", SYMBOL, Gene)]

# 调整 Gene 的显示顺序，让画出来的条形图从上到下更符合阅读习惯。
top20_plot[, DisplayGene := factor(DisplayGene, levels = rev(DisplayGene))]

# 保存“前 10 差异基因”的柱状图。
ggsave(
  filename = file.path(fig_dir, "top10_differential_genes.png"),
  plot = ggplot(top20_plot, aes(x = DisplayGene, y = LogFC, fill = LogFC > 0)) +
    geom_col(show.legend = FALSE) +
    coord_flip() +
    scale_fill_manual(values = c("#4e79a7", "#e15759")) +
    labs(
      title = "Top 10 Differential Genes in Training Set",
      x = "Gene Symbol / Ensembl ID",
      y = "Mean Difference (Tumor - Normal)"
    ) +
    theme_minimal(base_size = 12),
  width = 9, height = 5.5, dpi = 150
)

# 再画一张“决策树最重要的前 10 个基因”图。
# 同样优先显示 Symbol，目的是让报告里直接展示可读的基因名称。
importance_plot <- as.data.table(tree_importance_with_symbol[1:min(10, nrow(tree_importance_with_symbol)), ])
importance_plot[, DisplayGene := Gene]
importance_plot[, DisplayGene := factor(DisplayGene, levels = rev(DisplayGene))]

ggsave(
  filename = file.path(fig_dir, "decision_tree_variable_importance_top10.png"),
  plot = ggplot(importance_plot, aes(x = DisplayGene, y = Importance)) +
    geom_col(fill = "#59a14f") +
    coord_flip() +
    labs(
      title = "Top 10 Important Genes in Decision Tree",
      x = "Gene Symbol / Ensembl ID",
      y = "Importance"
    ) +
    theme_minimal(base_size = 12),
  width = 9, height = 5.5, dpi = 150
)

# 下面做 PCA 可视化。
# PCA 可以粗略理解成：把高维数据压缩到 2 维，方便画图看 Tumor 和 Normal 是否分开。

# 从完整样本中取出 Top50 基因表达。
top50_all <- expr_mat[top50_genes, , drop = FALSE]

# 再次转置成“每行一个样本，每列一个基因”。
pca_input <- t(top50_all)

# 计算每个基因在当前数据中的标准差。
gene_sd <- apply(pca_input, 2, sd)

# 去掉方差为 0 的基因。
# 否则 prcomp 做标准化时会报错。
pca_input <- pca_input[, gene_sd > 0, drop = FALSE]

# 真正执行 PCA。
# center = TRUE 表示先减去均值
# scale. = TRUE 表示再除以标准差
pca_obj <- prcomp(pca_input, center = TRUE, scale. = TRUE)

# 取前两个主成分坐标，整理成表格。
pca_df <- data.table(
  Sample = sample_info$Sample,
  Class = sample_info$Class,
  PC1 = pca_obj$x[, 1],
  PC2 = pca_obj$x[, 2]
)

# 保存 PCA 坐标表。
fwrite(pca_df, file.path(tab_dir, "pca_coordinates_top50.csv"))

# 保存 PCA 散点图。
ggsave(
  filename = file.path(fig_dir, "pca_top50.png"),
  plot = ggplot(pca_df, aes(x = PC1, y = PC2, color = Class)) +
    geom_point(size = 2.4, alpha = 0.85) +
    scale_color_manual(values = c("Normal" = "#4e79a7", "Tumor" = "#e15759")) +
    labs(title = "PCA of Top 50 Differential Genes") +
    theme_minimal(base_size = 12),
  width = 7.5, height = 5.5, dpi = 150
)

# 保存 ROC 曲线图。
ggsave(
  filename = file.path(fig_dir, "roc_curve_decision_tree.png"),
  plot = ggplot(roc_df, aes(x = fpr, y = tpr)) +
    geom_line(color = "#e15759", linewidth = 1.1) +
    geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "grey50") +
    annotate(
      "text",
      x = 0.68, y = 0.12,
      label = paste0("AUC = ", sprintf("%.4f", metrics$overall$AUC)),
      size = 4.2
    ) +
    labs(
      title = "ROC Curve of Decision Tree",
      x = "False Positive Rate",
      y = "True Positive Rate"
    ) +
    theme_minimal(base_size = 12),
  width = 6.6, height = 5.5, dpi = 150
)

# 保存决策树结构图。
# png() 打开一个图片设备，plot/text 往里面画，dev.off() 关闭图片设备。
png(file.path(fig_dir, "decision_tree_structure.png"), width = 1600, height = 1000, res = 150)
plot(tree_model, uniform = TRUE, margin = 0.08, branch = 0.4)
text(tree_model, use.n = TRUE, cex = 0.55)
dev.off()

# 把决策树的详细文字摘要保存成 txt 文件。
capture.output(summary(tree_model), file = file.path(tab_dir, "decision_tree_summary.txt"))

# 把最重要的运行结果整理成几行文字，方便快速查看。
summary_lines <- c(
  paste("Samples used:", ncol(expr_mat)),
  paste("Tumor samples:", sum(labels == "Tumor")),
  paste("Normal samples:", sum(labels == "Normal")),
  paste("Training samples:", length(train_idx)),
  paste("Testing samples:", length(test_idx)),
  paste("Accuracy:", sprintf("%.4f", metrics$overall$Accuracy)),
  paste("Precision:", sprintf("%.4f", metrics$overall$Precision)),
  paste("Recall:", sprintf("%.4f", metrics$overall$Recall)),
  paste("Specificity:", sprintf("%.4f", metrics$overall$Specificity)),
  paste("F1:", sprintf("%.4f", metrics$overall$F1)),
  paste("AUC:", sprintf("%.4f", metrics$overall$AUC))
)

# 把上面的摘要文字写入文件。
writeLines(summary_lines, file.path(out_dir, "run_summary.txt"))

# 终端提示：整个流程已经跑完。
message("TCGA homework analysis complete.")
