# پیوست ۲ و ۳ - جدول آمار توصیفی و محاسبه مقدار پی (R / RStudio)
# Descriptive statistics table (Table 1) stratified by CVD5, with p-values.
#
# install.packages("table1")
# install.packages("readxl")

library(table1)
library(readxl)

# preprocessed_data: the merged data after removing rows with missing values (N = 3277)
preprocessed_data <- read_excel("data/preprocessed_data.xlsx")

# ---- p-value function (Appendix 3) -----------------------------------------
# numeric variables      -> two-sample t-test
# categorical variables  -> chi-squared test of independence
pvalue <- function(x, ...) {
  y <- unlist(x)
  g <- factor(rep(1:length(x), times = sapply(x, length)))
  if (is.numeric(y)) {
    p <- t.test(y ~ g)$p.value
  } else {
    p <- chisq.test(table(y, g))$p.value
  }
  # the initial empty string places the output on the line below the variable label;
  # "<" is written as an HTML entity
  c("", sub("<", "&lt;", format.pval(p, digits = 3, eps = 0.001)))
}

# ---- Table 1 (Appendix 2) ---------------------------------------------------
tbl <- table1(
  ~ Age + factor(sex) + factor(DMHx) +
    factor(sbpcat2) + factor(sbpcat3) + factor(sbpcat4) +
    factor(WHR2) + factor(WHR3) + factor(WHR4) +
    Follow + factor(Sg3) + factor(Sg8) + factor(PHQ2) | factor(CVD5),
  data = preprocessed_data,
  extra.col = list(`P-value` = pvalue)
)

print(tbl)
