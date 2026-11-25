-- 1. Create a dedicated database for the Sales ETL project
CREATE DATABASE Sales_ETL_DB;
GO

USE Sales_ETL_DB;
GO

-- 2. Create schemas to organize raw and clean data layers
CREATE SCHEMA staging;
GO

CREATE SCHEMA sales;
GO

-- 3. Create core tables inside the 'sales' schema
CREATE TABLE sales.Customers (
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    email VARCHAR(150)
);

CREATE TABLE sales.Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    unit_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE sales.Orders (
    order_id INT PRIMARY KEY,
    customer_id INT FOREIGN KEY REFERENCES sales.Customers(customer_id),
    product_id INT FOREIGN KEY REFERENCES sales.Products(product_id),
    quantity INT NOT NULL,
    order_date DATE
);
GO
