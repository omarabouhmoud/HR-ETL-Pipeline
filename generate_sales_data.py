import os
import pandas as pd
from faker import Faker
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

# التأكد من وجود مجلد data
os.makedirs("data", exist_ok=True)

# 1. بيانات العملاء (مع تكرار وأخطاء مقصودة)
customers = []
for i in range(1, 31):
    customers.append({
        "customer_id": 100 + i,
        "full_name": fake.name() if random.random() > 0.10 else None,
        "city": random.choice(["Riyadh", "Jeddah", "Tabuk", "Dammam"]),
        "email": fake.email()
    })
customers.extend(customers[:2])  # تكرار مقصود

# 2. بيانات المنتجات
products = [
    {"product_id": 1, "product_name": "Laptop Pro", "category": "Electronics", "unit_price": 4500.00},
    {"product_id": 2, "product_name": "Wireless Mouse", "category": "Accessories", "unit_price": 120.00},
    {"product_id": 3, "product_name": "Mechanical Keyboard", "category": "Accessories", "unit_price": 350.00},
    {"product_id": 4, "product_name": "4K Monitor", "category": "Electronics", "unit_price": 1600.00}
]

# 3. بيانات الطلبات (مع كميات فارغة مقصودة)
orders = []
for i in range(1, 51):
    orders.append({
        "order_id": 1000 + i,
        "customer_id": random.randint(101, 130),
        "product_id": random.randint(1, 4),
        "quantity": random.randint(1, 5) if random.random() > 0.10 else None,
        "order_date": fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d")
    })

# حفظها في ملف Excel واحد داخل مجلد data
file_path = "data/raw_sales_data.xlsx"
with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
    pd.DataFrame(customers).to_excel(writer, sheet_name="Customers", index=False)
    pd.DataFrame(products).to_excel(writer, sheet_name="Products", index=False)
    pd.DataFrame(orders).to_excel(writer, sheet_name="Orders", index=False)

print(f"تم توليد الملف بنجاح في: {file_path}")
