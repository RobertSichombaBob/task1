# Codveda Technology – Data Science Internship (Level 1)

## Overview

Welcome to my submission for **Level 1** of the Codveda Data Science Internship.  
I have completed **all three tasks** with a dual approach:

- **Task 1 (Web Scraping)** – I built a **production‑grade full‑stack application** (FastAPI + Streamlit + Docker) and also provide a **Jupyter notebook** version for reproducibility.
- **Task 2 (Data Cleaning)** – A detailed notebook with outlier removal, encoding, and standardisation.
- **Task 3 (Exploratory Data Analysis)** – A PhD‑level notebook with statistical tests, PCA, and business insights.

Every task exceeds the basic requirements. The code is clean, documented, and ready for real‑world use.

---



---

## Task 1 – Data Collection & Web Scraping

### The Problem
Manually collecting data from websites is slow and error‑prone. I built an **automated scraping system** that extracts book information from `books.toscrape.com` (a practice‑friendly website) and serves it via a REST API with an interactive dashboard.


**Key Features**
- **Concurrent, polite scraping** – `ThreadPoolExecutor` with random delays (0.5–0.8 s) and user‑agent rotation to avoid blocking.
- **Resilience** – automatic retries (`tenacity`), timeouts, and logging.
- **FastAPI backend** – endpoints to trigger a scrape and retrieve paginated results.
- **Streamlit dashboard** – visualise, filter, sort, and export scraped books to CSV.
- **Dockerised** – run the whole system with `docker-compose up`.

- Run the task_1.ipynb notebook cell by cell in any Jupyter environment.

---



---

## Task 2 – Data Cleaning & Preprocessing

### The Problem
- Raw customer churn data (churn-bigml-80.csv) contains outliers, categorical variables, and unscaled numerical features – all of which must be fixed before machine learning.

### What I Did
- Handled missing data – demonstrated median imputation (dataset had none).

- Removed outliers using the Interquartile Range (IQR) method – eliminated 420 rows (15.8%).

- Encoded categorical variables – label encoding for International plan and Voice mail plan; one‑hot encoding for State.

- Standardised numerical features using StandardScaler (zero mean, unit variance).

### Key Outputs
- Outlier counts: Customer service calls had 210 outliers (7.9%), Total intl calls 66 outliers (2.5%).

- Shape change: from 2666×20 to 2246×69 after one‑hot encoding.

- Final cleaned dataset: churn_cleaned_preprocessed.csv (ready for modelling).

### How to Run
Open task_2.ipynb in Jupyter or VSCode and run all cells.
---



---

## Task 3 – Exploratory Data Analysis (PhD‑Level)
### The Problem
- Understanding why customers churn is critical for business. I performed an in‑depth statistical and visual analysis to uncover patterns, test hypotheses, and generate actionable recommendations.

### What I Did (Beyond Basic EDA)
- Advanced summary statistics – skewness, kurtosis, coefficient of variation.

- Outlier detection – IQR and Z‑score methods with visual confirmation.

- Hypothesis testing – t‑tests, chi‑square tests (all p‑values < 0.001 for churn‑related features).

- Correlation matrix with hierarchical clustering and a clustered heatmap.

- Principal Component Analysis (PCA) – reduced 16 numerical features to 2 dimensions.


### Key Insights
- PCA variance: The first two principal components explain only 25.5% of the variance (PC1=12.8%, PC2=12.7%). This is typical for datasets with many weakly correlated features; more components would be needed to capture the majority of variance.

#### Top churn drivers (correlation with Churn):

- International plan (encoded): +0.34

- Customer service calls: +0.32

- Total day minutes: +0.21

#### Protective factor: Voice mail plan (encoded): –0.15

#### Statistical significance: All numerical features except Area code differ significantly between churned and non‑churned customers (t‑test p < 0.001).

#### Chi‑square tests: International plan, Voice mail plan, and State are strongly associated with churn (p < 0.001).

### Business Recommendations
- Proactively contact customers with >5 service calls or >250 day minutes.

- Re‑evaluate the International plan – high churn suggests poor perceived value.

- Promote the Voice mail plan as a loyalty tool.

- For modelling: drop one of each minutes/charge pair, scale features, and use class weighting (churn is only 15%).

### How to Run
Open task_3.ipynb and execute all cells. The final report is saved as eda_insights_report.txt.