# MedCoder — Assistive Clinical NLP & ICD-10 Coding Platform

<div align="center">

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MLflow](https://img.shields.io/badge/MLflow-Registry-0194E2.svg?logo=mlflow&logoColor=white)](https://mlflow.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Tests: Pytest](https://img.shields.io/badge/tests-pytest-blue.svg?logo=pytest&logoColor=white)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

> **Assistive clinical NLP platform converting unstructured medical notes into ranked ICD-10-CM code suggestions via medical abbreviation expansion, hybrid dense-lexical retrieval, and human-in-the-loop audit workflows.**

---

## 📖 Executive Summary & Value Proposition

**`medcoder`** is a production-grade, end-to-end machine learning system built with strict engineering discipline, reproducible pipelines, and enterprise MLOps best practices. It bridges the gap between theoretical statistical rigor and high-availability operational microservices.

## 🩺 Core Methodologies & Clinical NLP

### 1. Clinical Note Preprocessing & Abbreviation Normalization
- Medical abbreviation expansion dictionary resolving ambiguous shorthand (e.g. *COPD*, *DM2*, *HTN*, *STEMI*) to canonical clinical terms.

### 2. Hybrid Dense-Lexical ICD-10 Retrieval
- Indexes official WHO/CMS ICD-10-CM code taxonomies (70,000+ codes).
- Combines BM25 token matching with clinical sentence embeddings using Reciprocal Rank Fusion to maximize Top-1, Top-5, and Top-10 recall.

### 3. Human-in-the-Loop Audit & Explainability
- Presents ranked code suggestions alongside clinical text justifications, hierarchy chapters, and exclusion notes for medical coder confirmation.

## 📊 Architecture & Pipeline

```mermaid
flowchart LR
    Note[Unstructured Clinical Note] --> Norm[Abbreviation Normalization]
    Norm --> Emb[Dense Clinical Embeddings + BM25]
    Emb --> RRF[Hybrid Code Retrieval Engine]
    RRF --> Rank[Top-K ICD-10 Code Suggestions]
    Rank --> Confirm[Human Coder Verification Harness]
    Confirm --> API[FastAPI :8150] --> UI[Streamlit Coding Workbench :8651]
```

## 🛠️ Tech Stack & Engineering Standards
- **NLP & Search:** Python 3.12, NumPy, SciPy, Sentence-Transformers, Rank-BM25
- **Serving & UI:** FastAPI, Streamlit, MLflow
- **Testing:** Pytest evaluation across Top-K accuracy benchmarks and abbreviation normalization


---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites & Environment Setup
Using **[uv](https://docs.astral.sh/uv/)** for lightning-fast, reproducible dependency resolution:

```bash
# Clone the repository
git clone https://github.com/jackson-marcus/medcoder.git
cd medcoder

# Install dependencies and pre-commit hooks
uv sync --group dev
```

### 2. Run Test Suite & Code Quality Checks
```bash
# Run unit & integration tests with coverage
uv run pytest --cov

# Run ruff linter and formatting checks
uv run ruff check .
uv run ruff format --check .
```

### 3. Launch Services Locally
```bash
# Start FastAPI REST API (listening on port :8150)
make api
# Or: uv run uvicorn medcoder.api.main:app --reload --port 8150

# Start interactive Streamlit dashboard (listening on port :8651)
make ui

# Launch local MLflow Experiment Tracking UI (listening on port :5016)
make mlflow
```

### 4. Run with Docker Compose
```bash
# Spin up the complete microservice stack
docker compose up --build
```

---

## 📂 Repository Layout

```
medcoder/
├── .github/workflows/ci.yml       # GitHub Actions CI pipeline (lint, test, build)
├── configs/                      # Configuration files and hyperparameters
├── data/                         # Data directory (raw, interim, processed)
├── scripts/                      # Data generators and operational scripts
├── src/medcoder/               # Core Python package
│   ├── api/                      # FastAPI routes, schemas, and endpoints
│   ├── models/                   # Statistical models, ML algorithms, and estimators
│   ├── ui/                       # Streamlit interactive application
│   └── settings.py               # Centralized configuration & environment loader
├── tests/                        # Comprehensive Pytest suite
├── docker-compose.yml            # Multi-service container orchestration
├── Dockerfile                    # Container definition for API service
├── Makefile                      # Standardized project tasks
└── pyproject.toml                # Pinned dependencies and tool configs
```

---

## 👤 Author & Contact

**Jackson Marcus**
- **Email:** [jackson.marcus.work@gmail.com](mailto:jackson.marcus.work@gmail.com)
- **Upwork:** [Jackson Marcus on Upwork](https://www.upwork.com/freelancers/~012235717501ad9c7b)
- **GitHub:** [@jackson-marcus](https://github.com/jackson-marcus)

*Available for machine learning engineering, MLOps, data science, and AI system architecture consulting and contract engagements.*

