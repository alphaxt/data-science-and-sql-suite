# 📊 Data Science & SQL Engineering Portfolio Suite

[![Python](https://img.shields.io/badge/Language-Python%203.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1?style=flat&logo=mysql&logoColor=white)](https://mysql.com)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/DevOps-Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

A unified **Data Science, Relational Database & NLP Engineering Suite** demonstrating the end-to-end data lifecycle: from **Enterprise Database Design (35 normalized tables, views, stored procedures, triggers)** to **Predictive Machine Learning Modeling**, **NLP Text Classification**, and **Production API Microservices with Automated CI/CD**.

---

## 🧭 Systems Overview & Capability Matrix

| Module | Core Domain | Technologies | Core Concepts & Techniques | Deliverables & Live Links |
| :--- | :--- | :--- | :--- | :--- |
| **`1-machine-learning-projects`** | **Predictive Modeling & EDA** | Scikit-Learn, Pandas, NumPy, Seaborn, Matplotlib | • Feature engineering & cross-validation<br>• Regression (Car price valuation)<br>• Time-series & demographic EDA (Unemployment)<br>• Multi-class classification (Iris flower) | Documented Jupyter Notebooks with publication-ready plots |
| **`2-nlp-spam-detector-streamlit`** | **Natural Language Processing (NLP)** | Python, NLTK, TF-IDF, Naive Bayes / SVM, Streamlit | • Text normalization, stopword filtering & vectorization<br>• High-precision binary spam classification<br>• Real-time web inference dashboard | 🌐 **[Live Streamlit App](https://alphaxt-spam-detector.streamlit.app/)** |
| **`3-retail-ecommerce-database`** | **Enterprise Relational Database Design** | MySQL, Relational Algebra, ERD, SQL DDL/DML | • 35 normalized tables (3NF / BCNF)<br>• Complex window functions, CTEs & multi-table joins<br>• Automated triggers, auditing logs & stored procedures<br>• ACID transaction integrity | Production SQL scripts, ERD schemas & analytical query suite |
| **`4-emotion-detector-microservice`** | **Containerized NLP Microservice** | Flask, IBM Watson NLU, Pytest, Docker, GitHub Actions | • Emotion scoring (joy, anger, sadness, fear, disgust)<br>• Keyword fallback heuristic engine<br>• REST API endpoints + HTML UI bars<br>• Automated CI/CD test pipeline & Dockerization | Docker container, JSON API & GitHub Actions CI |

---

## 📂 Suite Directory Structure

```text
data-science-and-sql-suite/
├── .gitignore
├── .gitattributes
├── LICENSE
├── README.md                                # Suite master documentation
│
├── 1-machine-learning-projects/             # Module 1: Exploratory Data Analysis & ML
│   ├── iris-flower-classification/          # Multi-class classification (KNN, Decision Trees)
│   ├── unemployment-analysis/               # Economic macro analysis & seasonal trends
│   └── car-price-prediction/                # Regression models & feature correlation
│
├── 2-nlp-spam-detector-streamlit/           # Module 2: Production NLP Web Application
│   ├── app/                                 # Streamlit UI & inference scripts
│   ├── dataset/                             # SMS / Email labeled text corpora
│   ├── Email_Spam_Detection.ipynb           # Model training, vectorization & evaluation
│   └── README.md
│
├── 3-retail-ecommerce-database/             # Module 3: Enterprise MySQL Relational Architecture
│   ├── database/                            # Schema definitions (35 normalized tables)
│   ├── queries/                             # Complex analytic queries, joins & aggregates
│   ├── advanced/                            # Stored procedures, triggers, views & indexing
│   ├── diagrams/                            # Entity Relationship Diagrams (ERD)
│   └── README.md                            # Comprehensive database documentation
│
└── 4-emotion-detector-microservice/         # Module 4: Containerized Flask NLP API & CI
    ├── app.py / wsgi.py                     # Flask application entry point
    ├── src/                                 # Watson NLU client & fallback heuristic engine
    ├── tests/                               # Pytest unit & integration test suite
    ├── Dockerfile                           # Production container specification
    ├── .github/workflows/                   # Automated GitHub Actions test pipeline
    └── README.md
```

---

## 🔬 In-Depth Module Highlights

### 1. 🏬 Retail & E-Commerce Management Database (`3-retail-ecommerce-database`)
Designed to mirror enterprise retail inventory, fulfillment, and customer management operations:
- **35 Tables in 3NF/BCNF:** Segregating orders, inventory batches, suppliers, customer tiers, shipments, and discount structures.
- **Advanced Stored Procedures & Triggers:** Automated re-order triggers when stock breaches thresholds, real-time inventory locking, and audit logs.
- **Business Intelligence Analytics:** Monthly recurring revenue, customer cohort lifetime value (LTV), inventory turnover velocity, and cart abandonment metrics.

### 2. 🛡️ NLP Email & SMS Spam Detector (`2-nlp-spam-detector-streamlit`)
- **End-to-End NLP Pipeline:** Raw text cleaning, punctuation removal, tokenization, stemming/lemmatization, and TF-IDF matrix representation.
- **Production Web Interface:** Deployed on Streamlit Cloud, allowing users to paste any email or message to receive real-time confidence scores and spam probabilities.

### 3. 🧠 Emotion Detection Service (`4-emotion-detector-microservice`)
- **Dual-Engine Architecture:** Integrates with IBM Watson NLU for contextual sentiment and emotion classification, with an automated keyword fallback for offline reliability.
- **Production Engineering:** Includes automated test suites run through `pytest`, linting configurations, Docker build scripts, and GitHub Actions CI.

---

## ⚡ Quick Start Guide

### Running the NLP Spam Detector (Streamlit)
```bash
cd 2-nlp-spam-detector-streamlit
pip install -r app/requirements.txt   # or streamlit pandas scikit-learn
streamlit run app/app.py
```

### Running the Emotion Detection Microservice (Flask / Docker)
```bash
cd 4-emotion-detector-microservice
# Run directly:
pip install -r requirements.txt
python app.py

# Or run with Docker:
docker build -t emotion-detector .
docker run -p 5000:5000 emotion-detector
```

### Loading the E-Commerce SQL Database (MySQL)
```bash
cd 3-retail-ecommerce-database
mysql -u root -p < database/schema.sql
mysql -u root -p < database/sample_data.sql
```

---

## 👤 Author

**Muhammad Danish**
- **GitHub:** [@alphaxt](https://github.com/alphaxt)
- **LinkedIn:** [Muhammad Danish](https://www.linkedin.com/in/muhammad-danish1/)
- **Degree:** B.S. Data Science @ University of Central Punjab (UCP)

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
