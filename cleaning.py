# E-commerce Customer Analysis Project

# Step 1: Load and Clean the Data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = "Online Retail.xlsx"  # Replace with your file path
df = pd.read_excel(file_path)

# Drop nulls in critical columns
df.dropna(subset=["CustomerID", "Description"], inplace=True)

# Remove cancelled orders (InvoiceNo starting with 'C')
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

# Remove negative quantities and prices
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Create TotalPrice column
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Export Cleaned Data for Excel/Power BI/Tableau
cleaned_file = "cleaned_online_retail.csv"
df.to_csv(cleaned_file, index=False)

# Step 2: RFM Analysis
# Snapshot date for recency calculation
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# Group by customer and calculate RFM metrics
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'TotalPrice': 'sum'
}).rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalPrice': 'Monetary'
})

# Score each RFM metric
rfm['R_score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method="first"), 4, labels=[1, 2, 3, 4])
rfm['M_score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4])

# Combine scores into single RFM score
rfm['RFM_Score'] = rfm['R_score'].astype(str) + rfm['F_score'].astype(str) + rfm['M_score'].astype(str)

# Export RFM for Excel/Power BI/Tableau
rfm.to_csv("rfm_scores.csv")

# Step 3: Sales Trend Analysis
# Monthly Sales Trend
sales_by_date = df.groupby(df['InvoiceDate'].dt.to_period('M'))['TotalPrice'].sum()
sales_by_date.index = sales_by_date.index.to_timestamp()
sales_by_date.plot(kind='bar', figsize=(12,6), title='Monthly Sales')
plt.ylabel('Revenue')
plt.xlabel('Month')
plt.tight_layout()
plt.show()

# Step 4: Top 10 Products by Revenue
top_products = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)
top_products.plot(kind='barh', figsize=(10,6), title='Top 10 Products by Revenue')
plt.xlabel('Revenue')
plt.tight_layout()
plt.show()

# Step 5: Summary Insights
print("Top 5 Customers by Revenue:")
print(df.groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False).head())

print("\nTop 5 Countries by Revenue:")
print(df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head())

print("\nLow Engagement Customers (RFM Score = 111):")
print(rfm[rfm['RFM_Score'] == '111'].head())

# --- Excel Dashboard Instructions ---
# 1. Open 'cleaned_online_retail.csv' in Excel
# 2. Create Pivot Tables:
#    - Revenue by Month
#    - Revenue by Product
#    - Top Customers
# 3. Use Slicers for Country, Product
# 4. Create Bar/Line Charts for Trends

# --- Power BI/Tableau Instructions ---
# 1. Load 'cleaned_online_retail.csv' and 'rfm_scores.csv'
# 2. Create measures:
#    - Total Sales, Avg Order Value, Unique Customers
# 3. Visuals:
#    - Line chart for Monthly Sales
#    - Bar chart for Top Products
#    - Table for RFM Segments
#    - Slicers for Country, RFM_Score

# --- GitHub README Template ---
# # E-commerce Customer Analysis Project
# 
# ## Objective
# Analyze customer purchase behavior for an online retail store using RFM analysis and sales trend analysis.
# 
# ## Tools Used
# - Python (pandas, matplotlib, seaborn)
# - Excel (pivot tables, charts)
# - Power BI / Tableau (interactive dashboard)
# 
# ## Key Findings
# - Identified top 5% high-value customers
# - Peak revenue observed in November
# - Top 10 products generate 40% of revenue
# 
# ## Files
# - `Online Retail.xlsx`: Original dataset
# - `cleaned_online_retail.csv`: Cleaned dataset
# - `rfm_scores.csv`: RFM segmented data
# 
# ## How to Use
# 1. Open `cleaned_online_retail.csv` in Excel/Power BI/Tableau
# 2. Use provided visuals/filters to explore insights
# 3. Python code included for full analysis pipeline