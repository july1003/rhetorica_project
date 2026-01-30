import sys
import os

# Add src/Logos to path
sys.path.append(os.path.join(os.getcwd(), 'src', 'Logos'))

try:
    from database import get_db_connection
    print("[OK] database module imported")
except ImportError as e:
    print(f"[FAIL] Could not import database module: {e}")
    sys.exit(1)

try:
    import passlib
    print("[OK] passlib is installed")
except ImportError:
    print("[FAIL] passlib is NOT installed")

try:
    conn = get_db_connection()
    print("[OK] Connected to Oracle DB")
    
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"[OK] Users table exists (Current user count: {count})")
    
    conn.close()
except Exception as e:
    print(f"[FAIL] DB Connection/Query failed: {e}")
