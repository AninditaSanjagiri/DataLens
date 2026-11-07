
# 🔎 DataLens – CSV Dataset Insight & Task Recommender

**Turn raw CSV data into actionable insights with Generative AI.**

[![Live App](https://img.shields.io/badge/Live%20App-Open%20DataLens-176b57?style=for-the-badge)](https://datalens-insight.streamlit.app/)

**DataLens** is an AI-powered dataset analysis application built with Python and Streamlit. It helps users understand unfamiliar datasets, discover patterns, identify potential data-quality issues, and explore machine-learning possibilities through an interactive interface.

By combining traditional data analysis techniques with Generative AI, semantic embeddings, and synthetic data generation, DataLens brings multiple stages of the data science workflow into one application.

## 🚀 Live Application

**Try DataLens here:**

### https://datalens-insight.streamlit.app/

No local installation is required to explore the deployed application.

---

## ✨ Features

DataLens is organised around five core modules.

### 1. Dataset Profiling & ML Task Recommendation

Explore your dataset and understand its structure before building a machine-learning model.

- Automatic dataset profiling: rows, columns, data types, missing values and unique values.
- Visualisation of numerical and categorical column distributions.
- Automatic target-column inference.
- Machine-learning task recommendations:
  - Binary classification
  - Multi-class classification
  - Regression
  - Clustering and exploratory analysis
- Recommended machine-learning lifecycle steps, from data validation to deployment.

### 2. AI-Powered Pandas Assistant

Interact with your dataset using natural language.

- Ask questions about your CSV in plain English.
- Gemini generates Python/Pandas code to answer the query.
- Generated code is checked using Python AST-based validation before execution.
- Code runs against a copy of the selected DataFrame.
- Gemini explains the execution results in understandable language.

### 3. Semantic Column Grouping & Chart Interpretation

Discover relationships between columns using language embeddings and Generative AI.

- Generate semantic embeddings using `all-MiniLM-L6-v2`.
- Represent columns using their names, data types and sample values.
- Group semantically similar columns using Agglomerative Clustering with cosine distance.
- Use Gemini's vision capabilities to interpret selected data visualisations.

### 4. Synthetic Data Generation

Experiment with synthetic tabular data using CTGAN.

- Generate synthetic rows from selected dataset columns.
- Compare real and synthetic data distributions.
- Compare correlation structures.
- Evaluate downstream predictive utility using Train on Synthetic, Test on Real (TSTR), when a target is available.

### 5. Data Quality & Risk Analysis

Identify potential issues before using a dataset for machine learning.

- Identifier-like column detection.
- Sensitive-column screening using keyword-based and semantic checks.
- Classification target imbalance analysis.
- Duplicate-row detection.
- Constant-column detection.
- Missing-value analysis.
- Dataset readiness scoring.

---

## 🧠 Architecture & Workflow

DataLens follows a modular data analysis workflow:

```text
                CSV Dataset
                     |
                     v
          Dataset Profiling (U1)
                     |
          +----------+----------+
          |                     |
          v                     v
     ML Task              Data Distribution
 Recommendation              Analysis
          |
          v
     Pandas AI Assistant (U2)
          |
          v
 Semantic Column Grouping (U3)
          |
          v
 Synthetic Data Generation (U4)
          |
          v
 Data Quality & Risk Analysis (U5)
          |
          v
       Actionable Insights
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend / Application | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualisation | Matplotlib |
| Generative AI | Google Gemini API |
| AI Integration | Google Gen AI SDK |
| Semantic Embeddings | Sentence Transformers |
| Clustering | Scikit-learn, Agglomerative Clustering |
| Synthetic Data | CTGAN |
| Machine Learning Utilities | Scikit-learn |

---

## 📊 Supported Datasets

DataLens includes a dataset library with the following options:

| Dataset | Source | Analysis |
|---|---|---|
| Kepler Objects of Interest | NASA Exoplanet Archive | Planet candidate classification |
| TESS Objects of Interest | NASA Exoplanet Archive | Multi-class candidate analysis |
| Confirmed Exoplanets | NASA Exoplanet Archive | Exploratory analysis and clustering |
| Iris | Scikit-learn | Classification and exploratory analysis |

The application also supports user-provided CSV files.

For the built-in NASA datasets, DataLens checks for local dataset files first and can fetch data through the NASA Exoplanet Archive TAP service when required.

---

## ⚙️ Run Locally

Want to explore the source code or run DataLens on your own machine?

### Prerequisites

- Python 3.11
- Git
- A Google Gemini API key for AI-powered features

### 1. Clone the repository

```bash
git clone https://github.com/AninditaSanjagiri/DataLens.git
cd DataLens
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Create a `.streamlit` directory in the project root if it does not already exist.

Inside it, create `secrets.toml`:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Alternatively, configure the `GEMINI_API_KEY` environment variable or enter the key through the application's sidebar.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

---

## 📁 Project Structure

```text
DataLens/
│
├── app.py
├── requirements.txt
├── README.md
│
├── datasets/
│   └── Optional local CSV datasets
│
├── .streamlit/
│   └── secrets.toml
│
└── .gitignore
```

**Note:** Do not commit `.streamlit/secrets.toml`, `.env`, or your virtual environment to GitHub.

---

## ⚠️ Limitations & Considerations

- **LLM-generated code:** AST-based validation provides restricted execution checks, but it is not a hardened security sandbox.
- **AI-generated explanations:** Gemini's interpretations may be incomplete or inaccurate and should be reviewed.
- **Semantic clustering:** Similarity between column descriptions does not necessarily imply statistical or domain equivalence.
- **Synthetic data:** CTGAN-generated records may not preserve every statistical relationship or domain constraint.
- **Privacy:** Synthetic data is not automatically anonymous or privacy-preserving.
- **Readiness score:** The dataset readiness score is heuristic and should not be treated as a formal data-quality or compliance certification.
- **API requirements:** Gemini-powered features require a valid API key and network access.

---

## 🔮 Future Improvements

Potential directions for extending DataLens include:

- More advanced data-quality and anomaly detection.
- Additional synthetic data evaluation and privacy testing.
- Support for more tabular generative models.
- Improved target selection and data leakage detection.
- More comprehensive model benchmarking.
- Reproducible experiment tracking and downloadable analysis reports.

---

## 👩‍💻 Author

**Anindita Sanjagiri**

B.E. Computer Science – Artificial Intelligence & Analytics

MIT Art, Design and Technology University, Pune

**Project:** P10 – Generative AI Mini-Project

---

## 📄 License

This project is intended for educational and experimentation purposes. Add a repository licence if you wish to specify permissions for reuse and distribution.

---

<p align="center">
  **Explore your data. Discover patterns. Make better ML decisions.**
  <br/>
  <a href="https://datalens-insight.streamlit.app/">Launch DataLens →</a>
</p>
