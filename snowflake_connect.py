import snowflake.connector 
from dotenv import load_dotenv 
import os 
import logging 

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s | %(levelname)s | %(message)s') 
logger = logging.getLogger(__name__) 

load_dotenv() 

conn = snowflake.connector.connect( 
    user = os.getenv('SNOWFLAKE_USER'), 
    password = os.getenv('SNOWFLAKE_PASSWORD'), 
    account = os.getenv('SNOWFLAKE_ACCOUNT'), 
    warehouse = os.getenv('SNOWFLAKE_WAREHOUSE'), 
    database = os.getenv('SNOWFLAKE_DATABASE'), 
    schema = os.getenv('SNOWFLAKE_SCHEMA') 
    )

cursor = conn.cursor() 
cursor.execute('SELECT CURRENT_VERSION(), CURRENT_USER(), CURRENT_DATABASE()') 
row = cursor.fetchone() 
logger.info(f'Snowflake version : {row[0]}') 
logger.info(f'Logged in as : {row[1]}') 
logger.info(f'Active database : {row[2]}') 

cursor.close() 
conn.close()