![SupplyChain360]("C:\Users\6sukr\Downloads\supplychain360_banner.png")

# 🌍 SupplyChain360

**SupplyChain360** is a visual simulation tool for global supply chain optimization.  
It helps users simulate logistics paths, optimize routes by cost or time, and track KPIs across shipments.

---

## 🚀 Features

- 🗺️ Interactive global supply chain network graph (nodes & edges)
- 🚚 Shipment path simulation between supplier & retailer
- 💡 Optimization for **cost** or **time**
- ⚠️ Optional **random delay injection** for realistic disruption modeling
- 📊 KPI Dashboard to track:
  - Total simulations
  - Average cost and time
  - Delayed shipments
  - Most efficient route

---

## 📁 Folder Structure

SupplyChain360/
├── app.py
├── requirements.txt
└── data/
├── global_supply_chain_nodes.csv
└── global_supply_chain_edges.csv


---

## ▶️ Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/SupplyChain360.git
cd SupplyChain360
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

## 3. Run the app
```bash
streamlit run app.py
```
## 4. Simulate Your First Shipment
a) Use the dropdowns to select a Supplier and Retailer

b) Choose whether to optimize for Cost or Time

c) Optionally enable random delay injection

d) View the route and KPI metrics below

✅ Make sure the data/ folder with both CSVs is present before running the app.


