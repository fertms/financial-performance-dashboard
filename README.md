# 💰 Financial Performance Dashboard

End-to-end financial analysis project featuring a star schema data warehouse, 
SQL queries with DuckDB, Python visualizations and an interactive Power BI dashboard.

---

## 🔍 Business Questions Answered

- What is the overall revenue, profit and margin trend over 3 years?
- Which product categories drive the most revenue?
- How does performance vary across regions?
- Which are the top 10 products by revenue?
- How did Year-over-Year growth evolve?

---

## 💡 Key Insights

- **Services** category shows the highest profit margin across all years
- **Revenue grew consistently** from 2022 to 2024
- **East and West** regions lead in total revenue share
- Top 10 products account for a significant portion of total revenue

---

## 🏗️ Data Architecture

Star schema with 1 fact table and 5 dimension tables:
```
fact_transactions
├── dim_date        (1,096 rows — daily from 2022 to 2024)
├── dim_product     (20 rows — 4 categories)
├── dim_region      (5 rows)
├── dim_customer    (200 rows — 3 segments)
└── dim_salesperson (30 rows — 3 seniority levels)
```

---

## 🛠️ Tech Stack

| Tool | Usage |
|---|---|
| Python 3.12 | Data generation and analysis |
| pandas | Data manipulation |
| DuckDB | SQL queries on DataFrames |
| matplotlib / seaborn | Data visualization |
| Power BI | Interactive dashboard |
| Git | Version control |

---

## 📁 Project Structure
```
financial-performance-dashboard/
├── data/
│   ├── raw/              ← generated star schema tables
│   └── processed/        ← enriched fact table for Power BI
├── notebooks/
│   └── financial_analysis.ipynb  ← full analysis notebook
├── scripts/
│   └── generate_data.py  ← synthetic data generation
├── outputs/              ← exported charts
├── powerbi/
│   └── dashboard.pbix    ← Power BI dashboard
└── README.md
```

---

## ▶️ How to Run
```bash
# Clone the repository
git clone https://github.com/fertms/financial-performance-dashboard.git
cd financial-performance-dashboard

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install pandas numpy matplotlib seaborn duckdb openpyxl ipykernel faker

# Generate the dataset
cd scripts
python generate_data.py

# Open the notebook
cd ../notebooks
jupyter notebook financial_analysis.ipynb
```

---

## 📊 Dashboard Preview

Interactive Power BI dashboard featuring:
- KPI cards: Total Revenue, Total Profit, Profit Margin, Total Transactions
- Stacked bar chart: Monthly Revenue by Category
- Donut chart: Revenue Share by Region
- Line chart: Revenue Trend (2022–2024)
- Horizontal bar: Top 10 Products by Revenue
- Slicers: Year, Region, Category, Customer Segment