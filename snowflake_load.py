import pandas as pd 
from sqlalchemy import create_engine 
from dotenv import load_dotenv 
import os 
import logging 

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s | %(levelname)s | %(message)s') 
logger = logging.getLogger(__name__) 
load_dotenv() 
# Load the cleaned dataset 
df = pd.read_csv('retail_orders_clean.csv') 
logger.info(f'Rows loaded from CSV: {len(df)}') 
# Build Snowflake SQLAlchemy connection string
engine = create_engine( 
    f"snowflake://{os.getenv('SNOWFLAKE_USER')}:{os.getenv('SNOWFLAKE_PASSWORD')}" 
    f"@{os.getenv('SNOWFLAKE_ACCOUNT')}/{os.getenv('SNOWFLAKE_DATABASE')}" 
    f"/{os.getenv('SNOWFLAKE_SCHEMA')}?warehouse={os.getenv('SNOWFLAKE_WAREHOUSE')}" 
    ) 
# Load DataFrame to Snowflake 
df.to_sql( 
    'retail_orders', 
    engine, 
    if_exists = 'replace', 
    index = False, 
    method = 'multi', 
    chunksize = 500 
    ) 
logger.info(f'Loaded {len(df)} rows into Snowflake table: retail_orders') 
engine.dispose()