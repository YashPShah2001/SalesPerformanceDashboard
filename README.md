# 🛍️ Interactive Sales Dashboard

This repository contains a fully interactive Streamlit dashboard designed to analyze and visualize sales performance from an e-commerce orders dataset. It enables comprehensive exploration of key business metrics like profit, sales, discounts, and order volumes across time, product categories, and geographic regions.

## 📊 Features

- 📆 **Year-wise Filtering** – Choose one or more years (e.g., 2022, 2023) to filter the entire dashboard.
- 🌎 **Region & State Filters** – Cascading filters to view metrics at a national, regional, or state level.
- 💰 **Key Metrics** – Total Sales, Total Profit, and Total Orders with year-over-year comparisons.
- 📈 **Time Series Analysis** – Monthly trends for Sales and Profit with grouped bar charts.
- 🧮 **Dynamic Table** – Search, sort, and filter transaction-level data with conditional formatting.
- 📦 **Product Analysis** – Top and bottom performing products based on sales or profit.
- 🧠 **Business Insights** – Visualizations for:
  - Segment-wise and Category-wise performance
  - Discount impact on revenue
  - Yearly comparisons
- 📐 **EDA Charts** – Additional insights using Seaborn/Matplotlib for deeper exploration.

## 🚀 Getting Started

### 1. Install Dependencies/ Setup virtual environment

Make sure you have **Python 3.8 or higher** installed.

- Download Python: https://www.python.org/downloads/
- During installation, check the option: ✅ "Add Python to PATH"

### 2. Install streamlit and other packages

Once python is installed, install other required libraries.

```pip install streamlit pandas plotly seaborn matplotlib```

### 3. Clone the Repository

```bash
git clone https://github.com/yourusername/sales-dashboard.git
cd sales-dashboard
```

###  4. Run the dashboard

Navigate to the project folder and run:
```streamlit run ordersDashboard.py```

## Dashboard Highlights
- Summary metrics
  ![image](https://github.com/user-attachments/assets/b3b645a9-a0d7-4da6-a031-046d4147197d)

- Monthly trends
  ![image](https://github.com/user-attachments/assets/8c8b36bd-c91e-4b2d-a32c-950e26394ffd)

  
### Built with
- Streamlit
- Pandas
- Plotly
- Seaborn
- Matplotlib
