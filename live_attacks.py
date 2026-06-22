import psycopg2
import random
import time
from dotenv import load_dotenv
import os

load_dotenv()


countries = [
    'United States', 'Russia', 'China', 'North Korea', 'India', 'Brazil',
    'Canada', 'United Kingdom', 'Germany', 'Japan', 'Australia', 'France'
]

cities = {
    'United States': ['Ashburn', 'Chicago', 'San Francisco', 'New York', 'Dallas', 'Seattle'],
    'Russia': ['Moscow', 'St. Petersburg', 'Kazan'],
    'China': ['Beijing', 'Shanghai', 'Shenzhen', 'Hangzhou'],
    'North Korea': ['Pyongyang'],
    'India': ['Ludhiana', 'Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad'],
    'Brazil': ['Sao Paulo', 'Rio de Janeiro'],
    'Canada': ['Montreal', 'Toronto', 'Vancouver'],
    'United Kingdom': ['London', 'Manchester', 'Edinburgh'],
    'Germany': ['Frankfurt', 'Berlin', 'Munich'],
    'Japan': ['Tokyo', 'Osaka'],
    'Australia': ['Sydney', 'Melbourne'],
    'France': ['Paris', 'Lyon']
}
isps = ['Google LLC', 'Amazon.com', 'China Telecom', 'Reliance Jio', 'Microsoft Corporation', 'Tata']
statuses = ['Blocked', 'Failed Login', 'Malware Detected']
usernames = ['admin', 'root', 'administrator', 'system']

try:
    
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"), 
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"), 
        host=os.getenv("DB_HOST"), 
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()
    print("✅ Database Connected! Live Hacker Bot Started...\n")

    
    while True:
        # Generate random attack data
        ip = f"{random.randint(11, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        country = random.choice(countries)
        city = random.choice(cities[country])
        isp = random.choice(isps)
        status = random.choice(statuses)
        user = random.choice(usernames)

        
        insert_query = """
            INSERT INTO daily_security_logs (ip_address, country, city, isp, status, username)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (ip, country, city, isp, status, user))
        conn.commit()

        print(f"🔥 NEW THREAT LOGGED: IP {ip} from {city}, {country}")
        
        
        time.sleep(3)

except Exception as e:
    print("❌ Error:", e)
