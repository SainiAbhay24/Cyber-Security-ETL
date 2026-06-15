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
print("⏳ Pipeline chal rahi hai... Kripya wait karo...")

# 2. LOAD VAULT
load_dotenv()

try:
    # 3. DATABASE CONNECTION
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"), host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()
    logging.info("✅ Securely Connected to PostgreSQL Database!")

    # 4. EXTRACT: Sirf oh IPs labho jinha da ISP haje update nahi hoya (NULL hai)
    cursor.execute("SELECT ip_address FROM daily_security_logs WHERE isp IS NULL;")
    records = cursor.fetchall()
    
    if not records:
        logging.info("👍 No new IPs to process. Everything is up to date!")
        print("✅ Saare IPs da data pehlan hi update ho chuka hai! Koi nava IP nahi hai.")
    else:
        logging.info(f"🔍 Found {len(records)} new IPs to process.")
        print(f"🔍 {len(records)} nave IPs labhe ne. Data kadd reha haan...")
        
        # 5. TRANSFORM & LOAD (API Call te Error Handling)
        for row in records:
            ip = row[0]
            try:
                # API Call
                url = f"http://ip-api.com/json/{ip}"
                response = requests.get(url)
                data = response.json()
                
                # Check status
                if data['status'] == 'success':
                    country = data.get('country', 'Unknown')
                    city = data.get('city', 'Unknown')
                    isp = data.get('isp', 'Unknown')
                    
                    # Update Query
                    update_query = """
                        UPDATE daily_security_logs
                        SET country = %s, city = %s, isp = %s
                        WHERE ip_address = %s;
                    """
                    cursor.execute(update_query, (country, city, isp, ip))
                    conn.commit() # Save data
                    logging.info(f"🎯 Updated {ip}: {city}, {country} | ISP: {isp}")
                else:
                    logging.warning(f"⚠️ API API failed for IP {ip}: {data.get('message')}")
                
                # Pro-Tip: API ban na hove is layi 1.5 second da break (Rate Limiting)
                time.sleep(1.5) 
                
            except Exception as api_err:
                logging.error(f"❌ API call crashed for IP {ip}: {api_err}")

    # 6. CLEANUP
    cursor.close()
    conn.close()
    logging.info("🔌 Pipeline closed cleanly.")
    print("🏁 Pipeline Execution Complete! 'pipeline_run.log' file check karo.")

except Exception as db_err:
    logging.error(f"❌ Database connection failed: {db_err}")
    print("⚠️ Error aagya! Log file check karo.")