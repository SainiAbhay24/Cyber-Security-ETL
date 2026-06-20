# 🛡️ Cyber Security Command Center: Real-Time Threat Intelligence

![Power BI](https://img.shields.io/badge/PowerBI-F2C811?style=for-the-badge&logo=Power%20BI&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

## 📌 Project Overview
This project is an end-to-end **Data Engineering and Analytics pipeline** that simulates, stores, and visualizes real-time global cyber-attacks. It acts as a Security Operations Center (SOC) dashboard, providing actionable insights into malicious IPs, targeted regions, and vulnerable ISPs.

## 🏗️ System Architecture
1. **Data Generation (Python):** A custom Python script (`live_attacks.py`) acts as a bot, generating simulated live cyber-attack data (IPs, locations, ISPs, threat status).
2. **Database Storage (PostgreSQL):** The data is securely pushed into a local PostgreSQL database in real-time using `psycopg2` and environment variables for security.
3. **Data Visualization (Power BI):** Power BI connects directly to the PostgreSQL database to render a dark-themed, interactive live tracking map and matrices.

## 🚀 Key Features
- **🌍 Global Threat Map:** Real-time pinpointing of attack origins using geocoding.
- **📊 Top Targeted Regions:** Dynamic bar charts showcasing highly vulnerable countries and cities.
- **💻 Hacker Matrix Terminal:** A live-feed table tracking exact IPs, Usernames, and ISP breaches.
- **🔐 Secure Credentials:** Environment variable integration (`.env`) for enterprise-grade database security.
- **🎨 Dark Mode UI:** Designed with SOC principles to reduce eye strain and highlight critical alerts (Neon Green/Red UI).

## 🛠️ Tech Stack Used
- **Scripting & Automation:** Python 3, `psycopg2`, `python-dotenv`
- **Relational Database:** PostgreSQL, SQL
- **Business Intelligence:** Power BI Desktop
- **UI/UX:** Custom Hex styling (`#000000`), Transparent Visuals

## ⚙️ How to Run This Project
1. Clone this repository.
2. Set up a local PostgreSQL database named `API` and create a table `daily_security_logs`.
3. Create a `.env` file in the root directory with your DB credentials:
   ```env
   DB_NAME=API
   DB_USER=postgres
   DB_PASS=your_password
   DB_HOST=localhost
   DB_PORT=5432
