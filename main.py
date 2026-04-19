from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import mysql.connector

app = FastAPI(title="Retail Medallion API")


DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password":"admin123"
    , 
    "database": "sales_pipeline"
}

def fetch_from_db(query: str):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@app.get("/")
def home():
    return {"message": "Retail Medallion API is Running!"}

@app.get("/product_sales")
async def get_product_sales(product_code: Optional[str] = Query(None)):
  
    query = "SELECT * FROM gold_product_performance"
    if product_code:
        query += f" WHERE StockCode = '{product_code}'"
    
    data = fetch_from_db(query)
    if not data:
        raise HTTPException(status_code=404, detail="Product not found")
    return data