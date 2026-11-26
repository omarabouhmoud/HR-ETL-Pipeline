# 🚀 End-to-End Sales ETL Data Pipeline (Python & SQL Server)
# 🚀 مشروع هندسة البيانات: خط أنابيب بيانات المبيعات المتكامل

[English Version](#-english-version) | [النسخة العربية](#-النسخة-العربية)

---

<a name="-english-version"></a>
## 🇬🇧 English Version

### 📌 Project Overview
This project demonstrates an automated, idempotent **Extract, Transform, and Load (ETL)** data pipeline built with **Python** and **Microsoft SQL Server 2022**. It simulates a real-world data engineering workflow by generating raw, messy Excel datasets, cleaning and validating the records using **Pandas**, and loading them into a structured relational database schema (`Sales_ETL_DB`) while strictly enforcing referential integrity.

### 🛠️ Tech Stack & Tools
* **Programming Language:** Python 3.x
* **Data Manipulation & Generation:** `Pandas`, `OpenPyXL`, `Faker`
* **Database Engine:** Microsoft SQL Server 2022 (SSMS)
* **Database Connectivity:** `SQLAlchemy`, `pyodbc` (ODBC Driver 17 for SQL Server)
* **Version Control & Documentation:** Git, GitHub Desktop, Notion

### 📂 Project Structure
```text
├── data/
│   └── raw_sales_data.xlsx      # Synthetic multi-sheet raw Excel dataset
├── sql/
│   └── create_sales_tables.sql  # DDL script for database, schemas, and relational tables
├── scripts/
│   ├── generate_sales_data.py   # Generates synthetic data with intentional anomalies
│   └── sales_etl_pipeline.py    # Main ETL pipeline (Extract, Clean, Validate, Load)
└── README.md                    # Bilingual project documentation
```

### ⚙️ Pipeline Architecture & Workflow
1. **Database Architecture (`create_sales_tables.sql`):**
   * Created a dedicated database (`Sales_ETL_DB`) isolated from operational systems.
   * Implemented separated schemas (`staging` and `sales`) to follow enterprise data organization standards.
   * Built normalized relational tables (`sales.Customers`, `sales.Products`, `sales.Orders`) with Primary Key and Foreign Key constraints.
2. **Synthetic Data Generation (`generate_sales_data.py`):**
   * Generated realistic customer, product, and order records into a multi-sheet Excel workbook (`raw_sales_data.xlsx`) using `Faker`.
   * Intentionally injected data quality issues (duplicate IDs and `NULL` values) to simulate raw source data.
3. **ETL Execution (`sales_etl_pipeline.py`):**
   * **Extract:** Programmatically read multiple worksheets from `raw_sales_data.xlsx` into Pandas DataFrames.
   * **Transform:** Deduplicated primary keys, dropped records with missing critical attributes (`full_name`), imputed missing order quantities with default values, standardized date formats, and filtered orphaned records to protect Foreign Keys.
   * **Load (Idempotent):** Implemented a safe pre-load cleanup step (`DELETE`) in reverse hierarchical order so the pipeline can be re-executed safely without Primary Key violations, then loaded parent tables (`Customers`, `Products`) prior to the child table (`Orders`).

### 🚀 How to Run
1. **Set up the Database:** Open `create_sales_tables.sql` in **SSMS** and execute it to create `Sales_ETL_DB`, schemas, and tables.
2. **Install Dependencies:**
   ```bash
   pip install pandas openpyxl sqlalchemy pyodbc faker
   ```
3. **Generate Raw Data:**
   ```bash
   python scripts/generate_sales_data.py
   ```
4. **Run the ETL Pipeline:**
   ```bash
   python scripts/sales_etl_pipeline.py
   ```

---

<a name="-النسخة-العربية"></a>
## 🇸🇦 النسخة العربية

### 📌 نظرة عامة على المشروع
يوضح هذا المشروع بناء خط أنابيب بيانات مؤتمت وقابل لإعادة التشغيل (**Idempotent ETL Pipeline**) باستخدام لغة **Python** وقاعدة بيانات **Microsoft SQL Server 2022**. يحاكي المشروع بيئة عمل هندسة البيانات الواقعية عبر توليد ملفات Excel خام تحتوي على أخطاء مقصودة، ثم تنظيف البيانات والتحقق من جودتها باستخدام مكتبة **Pandas**، وضخها في قاعدة بيانات علائقية منظمة (`Sales_ETL_DB`) مع الحفاظ التام على سلامة الروابط المرجعية بين الجداول.

### 🛠️ التقنيات والأدوات المستخدمة
* **لغة البرمجة:** Python 3.x
* **معالجة وتوليد البيانات:** `Pandas`، `OpenPyXL`، `Faker`
* **قواعد البيانات:** Microsoft SQL Server 2022 (SSMS)
* **الربط والاتصال بقواعد البيانات:** `SQLAlchemy`، `pyodbc` (ODBC Driver 17 for SQL Server)
* **إدارة الأكواد والتوثيق:** Git، GitHub Desktop، Notion

### ⚙️ آلية عمل خط الأنابيب (Workflow)
1. **هيكلة قاعدة البيانات (`create_sales_tables.sql`):**
   * إنشاء قاعدة بيانات مستقلة (`Sales_ETL_DB`) معزولة تماماً عن الأنظمة الأخرى.
   * تقسيم القاعدة إلى مخططات منظمة (`staging` و `sales`) لتطبيق معايير تنظيم طبقات البيانات.
   * بناء الجداول العلائقية (`sales.Customers`، `sales.Products`، `sales.Orders`) مع تفعيل قيود المفاتيح الأساسية والأجنبية (`Primary & Foreign Keys`).
2. **توليد البيانات الوهمية (`generate_sales_data.py`):**
   * توليد بيانات عملاء ومنتجات وطلبات وحفظها في ملف إكسل متعدد الصفحات (`raw_sales_data.xlsx`) باستخدام مكتبة `Faker`.
   * إضافة أخطاء مقصودة (تكرار السجلات وقيم فارغة `NULL`) لمحاكاة فوضى البيانات الخام في الواقع.
3. **تنفيذ المعالجة والتحميل (`sales_etl_pipeline.py`):**
   * **الاستخراج (Extract):** قراءة أوراق العمل من ملف الإكسل وتحويلها إلى جداول `Pandas DataFrames`.
   * **التنظيف والتحويل (Transform):** إزالة التكرار لحماية المفاتيح الأساسية، حذف السجلات التي تفتقد بيانات جوهرية (مثل اسم العميل)، تعويض القيم الفارغة في الكميات، توحيد صيغ التواريخ، واستبعاد الطلبات غير المرتبطة بعملاء صالحين لحماية المفاتيح الأجنبية.
   * **التحميل الآمن (Idempotent Load):** تفريغ الجداول بالترتيب العكسي قبل التحميل لضمان إمكانية إعادة تشغيل السكربت مرات متعددة دون أخطاء تكرار، ثم تحميل الجداول الرئيسية (الأب) أولاً يليها الجدول التابع (الابن).
