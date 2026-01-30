import os
import oracledb
from dotenv import load_dotenv

# Load .env from project root (../../.env relative to this file)
# This assumes this file is in src/Logos/database.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "../../.env"))

def get_db_connection():
    """
    Establishes a connection to the Oracle Database.
    Returns a connection object or raises an exception.
    """
    try:
        host = os.getenv('ORACLE_HOST')
        port = os.getenv('ORACLE_PORT')
        service = os.getenv('ORACLE_SERVICE_NAME')
        user = os.getenv('ORACLE_USER')
        password = os.getenv("ORACLE_PASSWORD")
        
        if not all([host, port, service, user, password]):
            raise ValueError("Missing Oracle DB environment variables")

        dsn = f"{host}:{port}/{service}"
        conn = oracledb.connect(
            user=user,
            password=password,
            dsn=dsn
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Oracle DB: {e}")
        raise e
