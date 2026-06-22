import os
import time
import logging
import requests
import psycopg2
from dotenv import load_dotenv

# 1. LOGGING SETUP
logging.basicConfig(
    filename='pipeline_run.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("🚀 Starting Advanced Cyber ETL Pipeline...")
print("⏳ Pipeline are ready...")

# 2. LOAD VAULT (.env file)
load_dotenv()

try:
    # 3. DATABASE CONNECTION
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"), 
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"), 
        host=os.getenv("DB_HOST"), 
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()
    logging.info("✅ Securely Connected to PostgreSQL Database!")

    # 4. EXTRACT
    cursor.execute("SELECT ip_address FROM daily_security_logs WHERE isp IS NULL;")
    records = cursor.fetchall()
    
    if not records:
        logging.info("👍 No new IPs to process. Everything is up to date!")
        print("✅ IP are already updated.")
    else:
        logging.info(f"🔍 Found {len(records)} new IPs to process.")
        print(f"🔍 {len(records)} Find new IP")
        
        # 5. TRANSFORM & LOAD 
        for row in records:
            ip = row[0]
            try:
                url = f"http://ip-api.com/json/{ip}"
                response = requests.get(url, timeout=5) # 5-second timeout
                data = response.json()
                
                if data['status'] == 'success':
                    country = data.get('country', 'Unknown')
                    city = data.get('city', 'Unknown')
                    isp = data.get('isp', 'Unknown')
                    
                    update_query = """
                        UPDATE daily_security_logs
                        SET country = %s, city = %s, isp = %s
                        WHERE ip_address = %s;
                    """
                    cursor.execute(update_query, (country, city, isp, ip))
                    logging.info(f"🎯 Staged update for {ip}: {city}, {country} | ISP: {isp}")
                else:
                    logging.warning(f"⚠️ API failed for IP {ip}: {data.get('message')}")
                
                time.sleep(1.5) # Rate limiting
                
            except requests.exceptions.Timeout:
                logging.error(f"⏳ Timeout Error: API took too long for IP {ip}")
            except Exception as api_err:
                logging.error(f"❌ API call crashed for IP {ip}: {api_err}")

        # Batch Commit 
        conn.commit()
        logging.info("💾 All records successfully committed to the database in one batch!")

    # 6. CLEANUP
    cursor.close()
    conn.close()
    logging.info("🔌 Pipeline closed cleanly.")
    print("🏁 Pipeline Execution Complete! 'pipeline_run.log' file check.")

except Exception as db_err:
    logging.error(f"❌ Database connection failed: {db_err}")
    print("⚠️ Error! Log file check.")
