import pandas as pd 
from sqlalchemy import create_engine 
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv 
import os 
import logging 

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s | %(levelname)s | %(message)s') 
logger = logging.getLogger(__name__) 
load_dotenv() 
# Load the cleaned dataset 


df = pd.read_csv('retail_orders_clean_ronewa_ernest.csv') 
logger.info(f'Rows loaded from CSV: {len(df)}') 
# Build Snowflake SQLAlchemy connection string 
print(os.getenv('SNOWFLAKE_USER'))
print(os.getenv('SNOWFLAKE_PASSWORD'))
print(os.getenv('SNOWFLAKE_ACCOUNT'))
print(os.getenv('SNOWFLAKE_DATABASE'))
print(os.getenv('SNOWFLAKE_SCHEMA'))
print(os.getenv('SNOWFLAKE_WAREHOUSE'))


private_key_file = "rsa_key.p8"
with open(private_key_file, "rb") as key:
    p_key = serialization.load_pem_private_key(
        key.read(),
        password=None
    )

engine = create_engine(
    f"snowflake://{os.getenv('SNOWFLAKE_USER')}@{os.getenv('SNOWFLAKE_ACCOUNT')}/"
    f"{os.getenv('SNOWFLAKE_DATABASE')}/{os.getenv('SNOWFLAKE_SCHEMA')}?"
    f"warehouse={os.getenv('SNOWFLAKE_WAREHOUSE')}",
    connect_args={"private_key": p_key}
)
# Load DataFrame to Snowflake 

df.to_sql( 'retail_orders', 
          engine, 
          if_exists = 'replace', 
          index = False, 
          method = 'multi', 
          chunksize = 500 
          ) 
logger.info(f'Loaded {len(df)} rows into Snowflake table: retail_orders') 
engine.dispose()