# SentinelWAF

**SentinelWAF: An AI-Powered Adaptive Web Application Firewall for Intelligent and Adversarial Attack Detection**

## 1. Project Overview

SentinelWAF is a proposed hybrid Web Application Firewall (WAF) that combines machine-learning-based HTTP request classification with additional analysis of suspicious and potentially obfuscated web requests.

The initial implementation establishes an XGBoost classification baseline. Subsequent phases will introduce controlled payload decoding and normalization, reclassification, and structural verification for selected SQL Injection requests. The project will evaluate whether these additional stages improve detection of modified attacks while keeping false positives and processing overhead under control.

## 2. Problem Statement

Machine-learning-based WAFs can classify multiple web-attack categories, but detection may be affected by modified or obfuscated payloads. Additional adversarial analysis may help but can introduce incorrect transformations and overhead, while grammar-based verification is mainly suited to supported SQL Injection patterns. This project will develop and evaluate a hybrid WAF that combines AI classification, controlled analysis of suspicious payloads and structural SQL Injection verification, measuring whether the additional stages improve detection of modified attacks without unacceptable false positives or latency.

## 3. Objectives

1. Develop an XGBoost classifier for normal requests and selected web-attack categories.
2. Implement controlled decoding, normalization and reclassification for suspicious payloads.
3. Add structural verification for selected SQL Injection requests and combine its evidence with AI predictions.
4. Compare classifier-only and enhanced configurations on standard and modified payloads using detection metrics and processing overhead.

## 4. Proposed Architecture

### Phase 1: Machine-Learning Baseline

HTTP request → Request feature extraction → XGBoost classifier → Predicted class and evaluation results.

### Later Phases: Adaptive Analysis

HTTP request → Initial classification → Suspicious-request analysis → Decoding and normalization → Reclassification → SQL Injection structural verification, where applicable → Decision engine → ALLOW, BLOCK or REVIEW.

The decision thresholds and routing rules will be defined and evaluated during implementation.

## 5. Datasets

### Primary dataset: SR-BH 2020

Used to develop and evaluate the initial multiclass HTTP request classifier.

Dataset information: https://fkie-cad.github.io/COMIDDS/content/datasets/sr_bh_2020/

Dataset record: https://doi.org/10.7910/DVN/OGOIXX

### Separate robustness dataset: BCCC-SFU-SQLInj-2023

Reserved for later testing of detection performance on evasive SQL Injection queries. It will initially remain separate from the training data.

Dataset information: https://www.yorku.ca/research/bccc/ucs-technical/cybersecurity-datasets-cds/sql-injection-attack-bccc-sfu-sqlinj-2023/

Dataset versions, label mappings, preprocessing and split strategies will be documented before final evaluation.

## 6. Core Research Papers

1. Enhanced Web Payload Classification Using WAMM: An AI-Based Framework for Dataset Refinement and Model Evaluation. IEEE Access, 2026. DOI: 10.1109/ACCESS.2026.3685450.
2. Adversarial SQLi Detection Using Character-Level CNN and Reinforcement Learning. IEEE Transactions on Dependable and Secure Computing, 2026. DOI: 10.1109/TDSC.2026.3669652.
3. PROGESI: A PROxy Grammar to Enhance Web Application Firewall for SQL Injection Prevention. IEEE Access, 2024. DOI: 10.1109/ACCESS.2024.3438092.

These papers inform the proposed design. Their methods will not be assumed to be implemented in SentinelWAF unless explicitly developed and tested.

## 7. Evaluation Plan

The initial baseline will be evaluated using precision, recall, F1-score, confusion matrix and processing time.

Later configurations will be compared to measure:

- Detection performance on modified payloads.
- False-positive and false-negative rates.
- Per-request processing latency.
- The contribution of each additional analysis stage.

No performance claims will be made until experiments have been completed.

## 8. Technology Stack

- Python
- pandas and scikit-learn
- XGBoost
- FastAPI and Uvicorn for the planned request API
- Git and GitHub for version control

## 9. Project Status

**Current phase:** Phase 1, dataset inspection and baseline development.

The baseline model and evaluation results are pending execution on the selected dataset.