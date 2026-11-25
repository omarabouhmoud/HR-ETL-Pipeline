import pandas as pd
from sqlalchemy import create_engine, text
import urllib

# 1. Configure SQL Server connection (Sales_ETL_DB)
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Sales_ETL_DB;"
    "Trusted_Connection=yes;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

print("1. Extracting raw data from Excel...")
file_path = "data/raw_sales_data.xlsx"
df_customers = pd.read_excel(file_path, sheet_name="Customers")
df_products = pd.read_excel(file_path, sheet_name="Products")
df_orders = pd.read_excel(file_path, sheet_name="Orders")

print("2. Cleaning and transforming data...")
# Clean Customers: remove duplicates and rows with missing full_name
df_customers = df_customers.drop_duplicates(subset=["customer_id"])
df_customers = df_customers.dropna(subset=["full_name"])

# Clean Products: remove duplicates
df_products = df_products.drop_duplicates(subset=["product_id"])

# Clean Orders: fill missing quantity with 1, standardize date, and validate Foreign Keys
df_orders = df_orders.drop_duplicates(subset=["order_id"])
df_orders["quantity"] = df_orders["quantity"].fillna(1).astype(int)
df_orders["order_date"] = pd.to_datetime(df_orders["order_date"]).dt.date

valid_customers = df_customers["customer_id"].tolist()
df_orders = df_orders[df_orders["customer_id"].isin(valid_customers)]

print("3. Clearing existing records to ensure idempotency...")
with engine.begin() as conn:
    conn.execute(text("DELETE FROM sales.Orders;"))
    conn.execute(text("DELETE FROM sales.Customers;"))
    conn.execute(text("DELETE FROM sales.Products;"))

print("4. Loading clean data into SQL Server...")
# Load parent tables first, then child table
df_customers.to_sql("Customers", con=engine, schema="sales", if_exists="append", index=False)
df_products.to_sql("Products", con=engine, schema="sales", if_exists="append", index=False)
df_orders.to_sql("Orders", con=engine, schema="sales", if_exists="append", index=False)

print("ETL Pipeline completed successfully! Clean data loaded into Sales_ETL_DB.")
