# 📈 Customer Intelligence Platform

> **AI-Powered Customer Analytics · CLTV Forecasting · Churn Prevention · Smart Segmentation**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://the-customer-intelligence-platform.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.x-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Latest-green.svg)](https://xgboost.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🔗 Live Demo

👉 **[Launch App](https://the-customer-intelligence-platform.streamlit.app/)**

---

## 📌 Project Overview

The **Customer Intelligence Platform** is an end-to-end marketing data science project built on real UK e-commerce transaction data. It combines machine learning, customer behavior analysis, and business intelligence into a single interactive dashboard.

The platform answers 4 critical business questions:

| Question | Solution |
|---|---|
| Who are my most valuable customers? | Customer Segmentation (RFM + K-Means) |
| Which customers are about to leave? | Churn Prediction (XGBoost / Random Forest) |
| How much will each customer spend? | CLTV Forecasting (Regression Models) |
| What patterns drive our revenue? | Exploratory Data Analysis |

---

## 🗂️ Project Structure

```
marketing-ml-segmentation-churn-ltv/
│
├── 📓 Notebooks
│   ├── marketing_eda.ipynb            # Exploratory Data Analysis
│   ├── customer_segmentation.ipynb    # RFM Analysis + K-Means Clustering
│   ├── churn_prediction.ipynb         # Churn Classification Model
│   └── cltv_prediction.ipynb          # CLTV Regression Model
│
├── 📊 Data
│   ├── OnlineRetail.csv               # Raw dataset (from Kaggle)
│   ├── OnlineRetail_Cleaned.csv       # Cleaned transactions
│   └── RFM_dataset.csv                # Customer-level RFM features + Segments
│
├── 🤖 Models
│   ├── churn_best_model.pkl           # Best churn classifier
│   ├── churn_scaler.pkl               # Scaler for churn model
│   ├── cltv_best_model_1m.pkl         # CLTV model (1 month)
│   ├── cltv_best_model_3m.pkl         # CLTV model (3 months)
│   └── cltv_best_model_6m.pkl         # CLTV model (6 months)
│
├── 🌐 App
│   ├── app.py                         # Streamlit application
│   ├── image.jpg                      # Logo / branding image
│   └── requirements.txt               # Python dependencies
│
└── README.md
```

---

## 📊 Dataset

| Property | Value |
|---|---|
| **Source** | [UCI Online Retail Dataset — Kaggle](https://www.kaggle.com/datasets/vijayuv/onlineretail) |
| **Period** | December 2010 – December 2011 |
| **Records** | ~541,000 transactions |
| **Customers** | ~4,300 unique customers |
| **Countries** | 37 countries |
| **Key Columns** | InvoiceNo, CustomerID, InvoiceDate, Quantity, UnitPrice, Country |

---

## 🔬 Notebooks Explained

### 1. `marketing_eda.ipynb` — Exploratory Data Analysis
- Revenue trends over time (monthly, quarterly, seasonal)
- Top customers, top products, top countries by revenue
- Day-of-week and month-of-year patterns
- Transaction-level and customer-level distributions

### 2. `customer_segmentation.ipynb` — Segmentation
- Built **RFM features**: Recency, Frequency, Monetary + AvgOrderValue + CustomerLifetime + PurchaseRate + AvgBasketSize
- Applied **Elbow Method** to choose optimal K
- **K-Means Clustering** (K=4) to discover natural segments
- Labeled clusters using business logic into 4 segments:
  - 💎 **VIP** — High frequency, high spend, recently active
  - 🟢 **Regular** — Moderate activity, consistent buyers
  - 🟡 **Potential** — New or growing customers
  - 🔴 **Lost / At Risk** — Inactive, low engagement

### 3. `churn_prediction.ipynb` — Churn Classification
- Defined churn: customer inactive for more than 90 days
- Compared 6 models using **GridSearchCV + Pipeline**:
  - Logistic Regression, SVC, Decision Tree, Random Forest, KNN, XGBoost
- Handled class imbalance with `class_weight='balanced'` and `scale_pos_weight`
- Evaluated using **F1 Score** (best metric for imbalanced churn data)
- Best model saved as `churn_best_model.pkl`

### 4. `cltv_prediction.ipynb` — CLTV Forecasting
- Used **time-based split**: past behavior → predict future spending
- Trained 3 separate models for 1-month, 3-month, and 6-month horizons
- Compared 8 regression models using **GridSearchCV**:
  - Linear Regression, Ridge, Lasso, Decision Tree, Random Forest, Gradient Boosting, KNN, XGBoost
- Evaluated using **MAE** and **R²**
- Each model saved as `cltv_best_model_{N}m.pkl`

---

## 🤖 Models Summary

### Churn Prediction
| Metric | Value |
|---|---|
| Algorithm | XGBoost (Best) |
| Scoring | F1 Score |
| CV Folds | 5 |
| Class Imbalance | Handled via `scale_pos_weight` |
| Key Features | Frequency, Monetary, AvgOrderValue, CustomerLifetime |

### CLTV Forecasting
| Metric | Value |
|---|---|
| Algorithm | XGBoost / Random Forest (Best) |
| Scoring | Negative MAE |
| CV Folds | 5 |
| Horizons | 1 month, 3 months, 6 months |
| Key Features | Recency, Frequency, Monetary, AvgOrderValue, CustomerLifetime, PurchaseRate, AvgBasketSize |

---

## 🌐 Streamlit App Features

The app has **4 tabs**:

### 📊 Tab 1 — Exploratory Data Analysis
- KPI summary cards (transactions, revenue, customers, countries)
- Monthly revenue trend line chart
- Revenue by country, product, day of week, month, quarter
- Top 10 customers by revenue
- Filterable by country and year from the sidebar

### 🧠 Tab 2 — Customer Segmentation
- Segment distribution (pie chart + bar chart)
- Revenue contribution by segment
- Segment profile cards (count, revenue, avg LTV, avg orders)
- Full customer data table

### ⚠️ Tab 3 — Churn Prediction
- Input: Frequency, Monetary, Avg Order Value, Customer Tenure
- Output: Churn probability % + risk level (Low / Medium / High)
- Recommended marketing action based on risk level

### 💰 Tab 4 — CLTV Forecasting
- Input: All 7 RFM behavioral features + prediction period (1 / 3 / 6 months)
- Output: Predicted customer spend in dollars
- Customer value tier (High / Medium / Low) with recommended action

---

## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/marketing-ml-segmentation-churn-ltv.git
cd marketing-ml-segmentation-churn-ltv
```

### 2. Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the notebooks (in order)
```
1. marketing_eda.ipynb
2. customer_segmentation.ipynb
3. churn_prediction.ipynb
4. cltv_prediction.ipynb   (run 3 times: duration_months = 1, 3, 6)
```

### 5. Launch the app
```bash
streamlit run app.py
```

---

## 📦 Requirements

```txt
streamlit
pandas
numpy
matplotlib
seaborn
plotly
scikit-learn
xgboost
joblib
warnings
```

---

## 💡 Key Business Insights

- 📈 Revenue peaks in **November and December** (holiday season) — increase ad spend in Q4
- 🇬🇧 **United Kingdom** accounts for over 80% of total revenue
- 💎 A small group of **VIP customers** generates the majority of revenue (Pareto principle)
- 🔴 **Lost/At-Risk customers** represent a significant win-back opportunity
- 📊 **Thursday and Tuesday** are the highest-grossing days — ideal for campaign launches
- 💰 CLTV model reveals which customers deserve higher acquisition cost investment

---

## 🗺️ Skills Demonstrated

| Area | Skills |
|---|---|
| **Data Wrangling** | pandas, datetime parsing, feature engineering |
| **EDA** | matplotlib, seaborn, plotly, business insight extraction |
| **Machine Learning** | Scikit-learn, XGBoost, GridSearchCV, Pipeline, Cross-Validation |
| **Marketing Analytics** | RFM Analysis, Customer Segmentation, Churn Modeling, CLTV |
| **MLOps** | joblib model persistence, scaler persistence, modular notebooks |
| **Deployment** | Streamlit, Streamlit Cloud |
| **Software** | Git, GitHub, virtual environments |

---

## 👤 Author

**Abdallah Ibrahim**  
Data Science & AI Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/abdallah-ibrahim-mohamed-4556792a5)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/YOUR_USERNAME)

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and share.

---

> *"Turning raw transactions into customer intelligence — one model at a time."*
