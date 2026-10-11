# SentinelWAF Literature Review

## Paper 1: Enhanced Web Payload Classification Using WAMM: An AI-Based Framework for Dataset Refinement and Model Evaluation

- **Journal:** IEEE Access, Volume 14, 2026, pages 61512–61527
- **DOI:** https://doi.org/10.1109/ACCESS.2026.3685450
- **Role in SentinelWAF:** Primary reference for multiclass web attack classification and the use of XGBoost.

### Relevance

The paper presents a web-attack classification framework that uses dataset refinement, feature engineering and machine-learning models. Its reported work also examines SR-BH 2020 and discusses the effect of dataset quality on classification.

### Application to this project

SentinelWAF will use XGBoost as its initial classifier and evaluate it on a documented subset of SR-BH 2020.

### Difference in implementation

SentinelWAF will first establish a reproducible baseline. The WAMM paper's dataset-refinement pipeline and reported performance will not be assumed to be reproduced. Results will be measured independently.

## Paper 2: Adversarial SQLi Detection Using Character-Level CNN and Reinforcement Learning

- **Journal:** IEEE Transactions on Dependable and Secure Computing, Volume 23, Issue 3, 2026, pages 6906–6923
- **DOI:** https://doi.org/10.1109/TDSC.2026.3669652
- **Role in SentinelWAF:** Reference for handling adversarially modified SQL Injection payloads.

### Relevance

The paper investigates SQL Injection detection under adversarial modifications and describes a character-level CNN combined with reinforcement learning.

### Application to this project

SentinelWAF will investigate controlled decoding, normalization and reclassification of suspicious requests. A separate SQL Injection dataset will later be used to evaluate robustness.

### Difference in implementation

The initial SentinelWAF classifier is XGBoost, not the paper's CNN and reinforcement-learning pipeline. The paper's method will not be described as implemented unless it is independently developed.

## Paper 3: PROGESI: A PROxy Grammar to Enhance Web Application Firewall for SQL Injection Prevention

- **Journal:** IEEE Access, Volume 12, 2024, pages 107689–107703
- **DOI:** https://doi.org/10.1109/ACCESS.2024.3438092
- **Role in SentinelWAF:** Reference for grammar-based structural verification of SQL Injection.

### Relevance

PROGESI presents a proxy-grammar approach to SQL Injection prevention and examines detection of mutated SQL Injection attempts.

### Application to this project

A later SentinelWAF phase will investigate structural verification for selected SQL Injection requests and combine its result with the classifier's prediction.

### Difference in implementation

SentinelWAF will not claim to reproduce PROGESI's grammar or proxy implementation unless the corresponding method is implemented and evaluated.

## Combined Research Direction

The three papers motivate three complementary areas:

1. Multiclass classification of HTTP requests.
2. Analysis of suspicious or modified payloads.
3. Structural verification of selected SQL Injection requests.

SentinelWAF will evaluate these components incrementally. Its contribution will be assessed through controlled comparisons of the baseline and enhanced configurations, including recall, false positives, false negatives and processing latency.

The project will not claim improved robustness or real-world protection until experiments support those conclusions.