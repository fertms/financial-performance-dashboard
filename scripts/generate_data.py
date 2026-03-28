# Script para geração de dados financeiros simulados — Financial Performance Dashboard
import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path

fake = Faker("pt_BR")
np.random.seed(42)

OUTPUT = Path("../data/raw")
OUTPUT.mkdir(exist_ok=True)

# ── Dimensão: data (2022 a 2024) ──────────────────────────────────────────────
dates = pd.date_range("2022-01-01", "2024-12-31", freq="D")
dim_date = pd.DataFrame({
    "date_id"  : range(1, len(dates) + 1),
    "date"     : dates,
    "year"     : dates.year,
    "quarter"  : dates.quarter,
    "month"    : dates.month,
    "month_name": dates.strftime("%B"),
    "week"     : dates.isocalendar().week.astype(int),
    "day"      : dates.day,
    "weekday"  : dates.strftime("%A"),
    "is_weekend": dates.dayofweek >= 5,
})

# ── Dimensão: produto ─────────────────────────────────────────────────────────
categories = {
    "Software":   ["ERP License", "CRM License", "BI Tool", "Security Suite", "Cloud Storage"],
    "Hardware":   ["Laptop", "Server", "Monitor", "Printer", "Network Switch"],
    "Services":   ["Consulting", "Implementation", "Support", "Training", "Audit"],
    "Subscriptions": ["Basic Plan", "Pro Plan", "Enterprise Plan", "Add-on Pack", "API Access"],
}

products = []
pid = 1
for category, items in categories.items():
    for item in items:
        base_price = {
            "Software": np.random.uniform(500, 5000),
            "Hardware": np.random.uniform(800, 8000),
            "Services": np.random.uniform(2000, 20000),
            "Subscriptions": np.random.uniform(100, 2000),
        }[category]
        products.append({
            "product_id"  : f"P{str(pid).zfill(3)}",
            "product_name": item,
            "category"    : category,
            "unit_price"  : round(base_price, 2),
            "cost_pct"    : round(np.random.uniform(0.30, 0.65), 2),
        })
        pid += 1
dim_product = pd.DataFrame(products)

# ── Dimensão: região ──────────────────────────────────────────────────────────
dim_region = pd.DataFrame({
    "region_id"  : range(1, 6),
    "region"     : ["North", "South", "East", "West", "Central"],
    "country"    : ["USA"] * 5,
    "manager"    : [fake.name() for _ in range(5)],
})

# ── Dimensão: cliente ─────────────────────────────────────────────────────────
segments = ["Enterprise", "Mid-Market", "SMB"]
dim_customer = pd.DataFrame({
    "customer_id"  : [f"C{str(i).zfill(4)}" for i in range(1, 201)],
    "company_name" : [fake.company() for _ in range(200)],
    "segment"      : np.random.choice(segments, 200, p=[0.2, 0.3, 0.5]),
    "region_id"    : np.random.randint(1, 6, 200),
    "since_year"   : np.random.randint(2015, 2023, 200),
})

# ── Dimensão: vendedor ────────────────────────────────────────────────────────
dim_salesperson = pd.DataFrame({
    "salesperson_id": [f"S{str(i).zfill(3)}" for i in range(1, 31)],
    "name"          : [fake.name() for _ in range(30)],
    "region_id"     : np.random.randint(1, 6, 30),
    "seniority"     : np.random.choice(["Junior", "Mid", "Senior"], 30, p=[0.3, 0.5, 0.2]),
})

# ── Fato: transações ──────────────────────────────────────────────────────────
N = 5000
fact_transactions = pd.DataFrame({
    "transaction_id": [f"T{str(i).zfill(5)}" for i in range(1, N + 1)],
    "date_id"       : np.random.choice(dim_date["date_id"], N),
    "product_id"    : np.random.choice(dim_product["product_id"], N),
    "customer_id"   : np.random.choice(dim_customer["customer_id"], N),
    "salesperson_id": np.random.choice(dim_salesperson["salesperson_id"], N),
    "quantity"      : np.random.randint(1, 20, N),
})

# Calcula revenue e cost
fact_transactions = fact_transactions.merge(
    dim_product[["product_id", "unit_price", "cost_pct"]], on="product_id"
)
fact_transactions["revenue"] = (
    fact_transactions["quantity"] * fact_transactions["unit_price"]
).round(2)
fact_transactions["cost"] = (
    fact_transactions["revenue"] * fact_transactions["cost_pct"]
).round(2)
fact_transactions["profit"] = (
    fact_transactions["revenue"] - fact_transactions["cost"]
).round(2)
fact_transactions = fact_transactions.drop(columns=["unit_price", "cost_pct"])

# ── Salvar ────────────────────────────────────────────────────────────────────
dim_date.to_csv(OUTPUT / "dim_date.csv",             index=False, encoding="utf-8-sig")
dim_product.to_csv(OUTPUT / "dim_product.csv",       index=False, encoding="utf-8-sig")
dim_region.to_csv(OUTPUT / "dim_region.csv",         index=False, encoding="utf-8-sig")
dim_customer.to_csv(OUTPUT / "dim_customer.csv",     index=False, encoding="utf-8-sig")
dim_salesperson.to_csv(OUTPUT / "dim_salesperson.csv", index=False, encoding="utf-8-sig")
fact_transactions.to_csv(OUTPUT / "fact_transactions.csv", index=False, encoding="utf-8-sig")

print("Dimensões geradas:")
print(f"  dim_date:        {len(dim_date)} linhas")
print(f"  dim_product:     {len(dim_product)} linhas")
print(f"  dim_region:      {len(dim_region)} linhas")
print(f"  dim_customer:    {len(dim_customer)} linhas")
print(f"  dim_salesperson: {len(dim_salesperson)} linhas")
print(f"\nFato gerado:")
print(f"  fact_transactions: {len(fact_transactions)} linhas")
print(f"\nReceita total simulada: ${fact_transactions['revenue'].sum():,.0f}")