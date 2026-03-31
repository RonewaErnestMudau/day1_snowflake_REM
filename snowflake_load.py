import pandas as pd 
from sqlalchemy import create_engine
from dotenv import load_dotenv 
import os 
import logging 
from urllib.parse import quote_plus

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s | %(levelname)s | %(message)s') 
logger = logging.getLogger(__name__) 
load_dotenv() 

# Load the cleaned dataset
df = pd.read_csv('retail_orders_clean_ronewa_ernest_202603311107.csv') 

#fixing date formats
#df['order_date'] = pd.to_datetime(df['order_date'])
logger.info(f'Rows loaded from CSV: {len(df)}') 
"""
print("USER:", os.getenv('SNOWFLAKE_USER'))
print("ACCOUNT:", os.getenv('SNOWFLAKE_ACCOUNT'))

conn_str = (
    f"snowflake://{os.getenv('SNOWFLAKE_USER')}:{os.getenv('SNOWFLAKE_PASSWORD')}"
    f"@{os.getenv('SNOWFLAKE_ACCOUNT')}/{os.getenv('SNOWFLAKE_DATABASE')}"
    f"/{os.getenv('SNOWFLAKE_SCHEMA')}"
    f"?warehouse={os.getenv('SNOWFLAKE_WAREHOUSE')}"
)

print("CONNECTION STRING:", conn_str)"""
# Build Snowflake SQLAlchemy connection string 

password = quote_plus(os.getenv('SNOWFLAKE_PASSWORD'))

engine = create_engine(
    f"snowflake://{os.getenv('SNOWFLAKE_USER')}:{password}"
    f"@{os.getenv('SNOWFLAKE_ACCOUNT')}/{os.getenv('SNOWFLAKE_DATABASE')}"
    f"/{os.getenv('SNOWFLAKE_SCHEMA')}"
    f"?warehouse={os.getenv('SNOWFLAKE_WAREHOUSE')}"
)

# Load DataFrame to Snowflake  
df.to_sql( 
    'retail_orders', 
    engine, if_exists = 
    'replace', 
    index = False, 
    method = 'multi', 
    chunksize = 500 
    ) 
logger.info(f'Loaded {len(df)} rows into Snowflake table: retail_orders') 
engine.dispose()