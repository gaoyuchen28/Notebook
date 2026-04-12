#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(data.table)
  library(rpart)
  library(nnet)
})

set.seed(20260403)

dir.create("outputs", showWarnings = FALSE)
dir.create("outputs/figures", showWarnings = FALSE, recursive = TRUE)
dir.create("outputs/tables", showWarnings = FALSE, recursive = TRUE)

sample_per_class <- 5000
target_col <- "ProductChoice"

message("Loading data...")
dt <- fread("Purchase Prediction Dataset.csv")

# Keep a compact feature set to avoid unstable high-cardinality dummy expansion.
selected_cols <- c(
  "ProductChoice",
  "MembershipPoints",
  "ModeOfPayment",
  "PurchaseTenure",
  "Channel",
  "IncomeClass",
  "CustomerPropensity",
  "CustomerAge",
  "MartialStatus",
  "LastPurchaseDuration"
)

dt <- dt[, ..selected_cols]
dt <- na.omit(dt)

factor_cols <- c(
  "ProductChoice",
  "ModeOfPayment",
  "Channel",
  "CustomerPropensity",
  "MartialStatus"
)

for (col in factor_cols) {
  dt[[col]] <- as.factor(dt[[col]])
}

dt[, IncomeClass := as.numeric(IncomeClass)]

class_counts <- dt[, .N, by = ProductChoice][order(ProductChoice)]
fwrite(class_counts, "outputs/tables/class_counts_full.csv")

balanced_dt <- dt[, {
  take_n <- min(.N, sample_per_class)
  .SD[sample(.N, take_n)]
}, by = ProductChoice]

balanced_counts <- balanced_dt[, .N, by = ProductChoice][order(ProductChoice)]
fwrite(balanced_counts, "outputs/tables/class_counts_balanced.csv")

balanced_dt[, row_id := .I]
train_ids <- balanced_dt[, {
  .(row_id = sample(row_id, ceiling(.N * 0.7)))
}, by = ProductChoice]

train_dt <- balanced_dt[row_id %in% train_ids$row_id]
test_dt <- balanced_dt[!row_id %in% train_ids$row_id]

train_dt[, split := "train"]
test_dt[, split := "test"]

train_dt[, c("row_id") := NULL]
test_dt[, c("row_id") := NULL]

fwrite(train_dt[, .N, by = .(split, ProductChoice)], "outputs/tables/train_distribution.csv")
fwrite(test_dt[, .N, by = .(split, ProductChoice)], "outputs/tables/test_distribution.csv")

train_dt[, split := NULL]
test_dt[, split := NULL]

metric_summary <- function(actual, predicted) {
  actual <- factor(actual)
  predicted <- factor(predicted, levels = levels(actual))
  cm <- table(actual, predicted)
  accuracy <- sum(diag(cm)) / sum(cm)

  precision <- recall <- f1 <- setNames(numeric(length(levels(actual))), levels(actual))
  for (cls in levels(actual)) {
    tp <- cm[cls, cls]
    fp <- sum(cm[, cls]) - tp
    fn <- sum(cm[cls, ]) - tp
    precision[cls] <- if ((tp + fp) == 0) 0 else tp / (tp + fp)
    recall[cls] <- if ((tp + fn) == 0) 0 else tp / (tp + fn)
    f1[cls] <- if ((precision[cls] + recall[cls]) == 0) 0 else {
      2 * precision[cls] * recall[cls] / (precision[cls] + recall[cls])
    }
  }

  per_class <- data.table(
    class = names(precision),
    precision = as.numeric(precision),
    recall = as.numeric(recall),
    f1 = as.numeric(f1)
  )

  overall <- data.table(
    accuracy = accuracy,
    macro_precision = mean(per_class$precision),
    macro_recall = mean(per_class$recall),
    macro_f1 = mean(per_class$f1)
  )

  confusion_dt <- as.data.table(cm, keep.rownames = "actual")
  list(confusion = confusion_dt, per_class = per_class, overall = overall)
}

message("Training decision tree...")
tree_model <- rpart(
  ProductChoice ~ .,
  data = train_dt,
  method = "class",
  control = rpart.control(cp = 0.001, maxdepth = 8, minbucket = 30)
)

message("Training multinomial logistic regression...")
multinom_model <- multinom(
  ProductChoice ~ .,
  data = train_dt,
  trace = FALSE,
  MaxNWts = 50000
)

tree_pred <- predict(tree_model, newdata = test_dt, type = "class")
multinom_pred <- predict(multinom_model, newdata = test_dt, type = "class")
baseline_pred <- factor(
  rep(names(sort(table(train_dt$ProductChoice), decreasing = TRUE))[1], nrow(test_dt)),
  levels = levels(test_dt$ProductChoice)
)

tree_metrics <- metric_summary(test_dt$ProductChoice, tree_pred)
multinom_metrics <- metric_summary(test_dt$ProductChoice, multinom_pred)
baseline_metrics <- metric_summary(test_dt$ProductChoice, baseline_pred)

overall_metrics <- rbindlist(list(
  cbind(model = "majority_baseline", baseline_metrics$overall),
  cbind(model = "decision_tree", tree_metrics$overall),
  cbind(model = "multinomial_logistic", multinom_metrics$overall)
))
fwrite(overall_metrics, "outputs/tables/model_overall_metrics.csv")

fwrite(cbind(model = "decision_tree", tree_metrics$per_class), "outputs/tables/decision_tree_per_class_metrics.csv")
fwrite(cbind(model = "multinomial_logistic", multinom_metrics$per_class), "outputs/tables/multinomial_per_class_metrics.csv")
fwrite(cbind(model = "majority_baseline", baseline_metrics$per_class), "outputs/tables/baseline_per_class_metrics.csv")

fwrite(tree_metrics$confusion, "outputs/tables/decision_tree_confusion_matrix.csv")
fwrite(multinom_metrics$confusion, "outputs/tables/multinomial_confusion_matrix.csv")
fwrite(baseline_metrics$confusion, "outputs/tables/baseline_confusion_matrix.csv")

tree_importance <- data.table(
  feature = names(tree_model$variable.importance),
  importance = as.numeric(tree_model$variable.importance)
)[order(-importance)]
fwrite(tree_importance, "outputs/tables/tree_variable_importance.csv")

png("outputs/figures/class_distribution_balanced.png", width = 900, height = 600)
barplot(
  balanced_counts$N,
  names.arg = balanced_counts$ProductChoice,
  col = c("#4e79a7", "#f28e2b", "#59a14f", "#e15759"),
  main = "Balanced Sample Class Distribution",
  xlab = "ProductChoice",
  ylab = "Count"
)
dev.off()

png("outputs/figures/tree_variable_importance.png", width = 1000, height = 700)
barplot(
  rev(tree_importance$importance),
  names.arg = rev(tree_importance$feature),
  horiz = TRUE,
  las = 1,
  col = "#4e79a7",
  main = "Decision Tree Variable Importance",
  xlab = "Importance"
)
dev.off()

png("outputs/figures/decision_tree_plot.png", width = 1400, height = 900)
plot(tree_model, uniform = TRUE, branch = 0.4, margin = 0.1)
text(tree_model, use.n = TRUE, cex = 0.8)
dev.off()

capture.output(summary(tree_model), file = "outputs/tables/decision_tree_summary.txt")
capture.output(summary(multinom_model), file = "outputs/tables/multinomial_summary.txt")

message("Analysis complete.")
