import pandas as pd
import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1", 
        user="root", 
        password="admin123",
        database="sales_pipeline"
    )


print("Starting Bronze to Silver...")

df = pd.read_csv("data/bronze/online_retail.csv") 


df = df.dropna(subset=['CustomerID']) 
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

# Data Quality 
assert df['TotalAmount'].min() > 0, "Error: Found negative totals!"
print("Silver Layer Cleaned.")

#  SILVER TO GOLD 
print("Creating Gold Layer...")
gold_df = df.groupby('StockCode').agg({
    'Quantity': 'sum',
    'TotalAmount': 'sum',
    'UnitPrice': 'mean'
}).reset_index()
gold_df.columns = ['StockCode', 'TotalUnitsSold', 'TotalRevenue', 'AvgPrice']

# LOAD TO MYSQL 
conn = get_db_connection()
cursor = conn.cursor()


cursor.execute("TRUNCATE TABLE sales_silver")
cursor.execute("TRUNCATE TABLE gold_product_performance")

# Load Silver Data 
for _, row in df.iterrows():
    sql = "INSERT INTO sales_silver (StockCode, Quantity, InvoiceDate, UnitPrice, CustomerID, TotalAmount) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (row['StockCode'], row['Quantity'], row['InvoiceDate'], row['UnitPrice'], row['CustomerID'], row['TotalAmount']))

# Load Gold Data
for _, row in gold_df.iterrows():
    sql = "INSERT INTO gold_product_performance (StockCode, TotalUnitsSold, TotalRevenue, AvgPrice) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (row['StockCode'], row['TotalUnitsSold'], row['TotalRevenue'], row['AvgPrice']))

conn.commit()
cursor.close()
conn.close()
print("ETL Pipeline Complete! Data now is in MySQL.")
