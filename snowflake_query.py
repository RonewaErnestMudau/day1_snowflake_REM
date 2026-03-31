import pandas as pd 
from sqlalchemy import create_engine 
from dotenv import load_dotenv 
import os 
import logging 
from urllib.parse import quote_plus

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
load_dotenv() 

password = quote_plus(os.getenv('SNOWFLAKE_PASSWORD'))

engine = create_engine(
    f"snowflake://{os.getenv('SNOWFLAKE_USER')}:{password}"
    f"@{os.getenv('SNOWFLAKE_ACCOUNT')}/{os.getenv('SNOWFLAKE_DATABASE')}"
    f"/{os.getenv('SNOWFLAKE_SCHEMA')}"
    f"?warehouse={os.getenv('SNOWFLAKE_WAREHOUSE')}"
) 
# Query 1: Revenue by region 
df_region = pd.read_sql("""
     SELECT region, 
            SUM(revenue) AS total_revenue, 
            COUNT(*) AS order_count 
    FROM retail_orders 
    GROUP BY region 
    ORDER BY total_revenue DESC 
""", engine) 

logger.info("Revenue by Region:") 
print(df_region)

# Query 2: Monthly revenue trend 

df_monthly = pd.read_sql("""
    SELECT
        DATE_TRUNC('month', TO_DATE(order_date)) AS month,
        SUM(revenue) AS revenue
    FROM retail_orders
    GROUP BY DATE_TRUNC('month', TO_DATE(order_date))
    ORDER BY month
""", engine)
logger.info("Monthly Revenue:")
print(df_monthly)

# Query 3: Top 5 customers (stretch) 
# 
df_top = pd.read_sql(""" 
    SELECT customer_id, SUM(revenue) AS total_spent 
    FROM retail_orders 
    GROUP BY customer_id 
    ORDER BY total_spent DESC LIMIT 5 
""", engine) 

logger.info("Top 5 Customers:") 
print(df_top) 

engine.dispose()