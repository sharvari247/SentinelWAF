# SentinelWAF Dataset Notes

## 1. Primary Dataset: SR-BH 2020

**Purpose:** Training and initial evaluation of the HTTP request classification baseline.

- Dataset overview: https://fkie-cad.github.io/COMIDDS/content/datasets/sr_bh_2020/
- Dataset record: https://doi.org/10.7910/DVN/OGOIXX
- Expected CSV filename: `data_capec_multilabel.csv`
- Expected local path: `data/raw/data_capec_multilabel.csv`

The dataset contains HTTP traffic collected from a WordPress honeypot and uses multi-label CAPEC-style attack annotations. A request may be associated with multiple attack categories.

The documented dataset contains 907,814 requests: 525,195 normal and 382,619 anomalous.

## 2. Initial Classification Plan

The initial baseline will use a documented, reduced single-class label mapping to make multiclass XGBoost training manageable.

Candidate categories include:

- Normal
- SQL Injection
- OS Command Injection
- Path Traversal
- Protocol Manipulation
- Other Attack

This is a proposed mapping, not a final decision. It will be finalized after inspecting the actual CSV labels, class frequencies and overlaps.

Rows with ambiguous or unsupported labels must be handled consistently and documented. We will not silently convert every multi-label record into a single class without recording the rule.

## 3. Request-Time Features

Potential input fields include:

- HTTP method
- HTTP request target or URI
- HTTP protocol
- Request content type
- User-Agent
- Request body

Only information available when the request arrives should be used for prediction.

Response-side fields, including response status and response message, must not be used as model input. Doing so would cause target leakage because these fields are not normally known before the WAF makes its decision.

## 4. Preprocessing and Data Splitting

Before training, the inspection script will report:

- CSV columns and sample rows
- Missing values
- Label-column names and class counts
- Whether requests have multiple labels
- Available request-time fields

The train, validation and test split must be documented. Related or duplicate requests across splits can make evaluation overly optimistic, so duplicates and possible data leakage will be investigated.

## 5. Label Quality and Limitations

Published work on SR-BH 2020 has reported potential inconsistencies in some labels. Initial metrics will therefore be interpreted as performance against the selected dataset annotations, not as proof of real-world WAF effectiveness.

Any filtering, label corrections or exclusions will be recorded with their rationale.

## 6. Separate Robustness Dataset

**BCCC-SFU-SQLInj-2023**

Official source: https://www.yorku.ca/research/bccc/ucs-technical/cybersecurity-datasets-cds/sql-injection-attack-bccc-sfu-sqlinj-2023/

This dataset is reserved for a later SQL Injection robustness experiment. It will initially remain separate from baseline training and will not be used to tune the model before its first evaluation.

The exact file format, labels, licensing and preprocessing requirements must be checked before use.

## 7. Dataset Status

- [ ] Download SR-BH 2020
- [ ] Verify the CSV filename and columns
- [ ] Inspect class distribution and multi-label records
- [ ] Finalize the label mapping
- [ ] Document train, validation and test splitting
- [ ] Train and evaluate the initial baseline
- [ ] Prepare a separate robustness evaluation using BCCC-SFU-SQLInj-2023