import pandas as pd
from sqlalchemy import create_engine
import urllib

# 1. إعداد الاتصال بقاعدة بيانات SQL Server المحلية (Sales_ETL_DB)
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Sales_ETL_DB;"
    "Trusted_Connection=yes;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

print("1. جاري استخراج البيانات من ملف Excel...")
file_path = "data/raw_sales_data.xlsx"
df_customers = pd.read_excel(file_path, sheet_name="Customers")
df_products = pd.read_excel(file_path, sheet_name="Products")
df_orders = pd.read_excel(file_path, sheet_name="Orders")

print("2. جاري تنظيف وتحويل البيانات (Transform)...")
# تنظيف جدول العملاء: حذف التكرار وحذف الصفوف التي بدون اسم
df_customers = df_customers.drop_duplicates(subset=["customer_id"])
df_customers = df_customers.dropna(subset=["full_name"])

# تنظيف جدول المنتجات: التأكد من عدم وجود تكرار
df_products = df_products.drop_duplicates(subset=["product_id"])

# تنظيف جدول الطلبات: تعويض الكمية الفارغة بـ 1، والتأكد من أن رقم العميل موجود ضمن العملاء النظيفين
df_orders = df_orders.drop_duplicates(subset=["order_id"])
df_orders["quantity"] = df_orders["quantity"].fillna(1).astype(int)
df_orders["order_date"] = pd.to_datetime(df_orders["order_date"]).dt.date

# فلترة الطلبات لضمان عدم حدوث خطأ Foreign Key بسبب العملاء المحذوفين
valid_customers = df_customers["customer_id"].tolist()
df_orders = df_orders[df_orders["customer_id"].isin(valid_customers)]

print("3. جاري تحميل البيانات إلى SQL Server بالترتيب الصحيح (Load)...")
# تحميل الجداول الأب أولاً ثم الجدول الابن
df_customers.to_sql("Customers", con=engine, schema="sales", if_exists="append", index=False)
df_products.to_sql("Products", con=engine, schema="sales", if_exists="append", index=False)
df_orders.to_sql("Orders", con=engine, schema="sales", if_exists="append", index=False)

print("تمت عملية الـ ETL بنجاح تام! تم ضخ جميع البيانات النظيفة في قاعدة Sales_ETL_DB.")
