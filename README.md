Smart Aware Air Quality System
A custom Streamlit dashboard for monitoring and forecasting air quality. This tool takes raw pollutant data and turns it into easy-to-read gauges, charts, and health alerts.

🛠️ Setup & Installation
1.Clone this folder to your computer.
2.Install the dependencies using terminal/command prompt:

pip install -r requirements.txt

Run the dashboard:
streamlit run app.py

📂 What's in this Repo?
app.py: The main Python script containing the dashboard logic and UI.
requirements.txt: The list of libraries (Streamlit, Pandas, etc.) needed to run the app.
models/: Folder containing the trained .pkl or .joblib files for AQI forecasting.
Bengaluru.csv: Sample dataset used for testing the visualizations.

🚀 Features
Admin Login: Secure access to the dashboard (Password: admin123).
Live AQI Gauge: Real-time visual for air quality levels.
Pollutant Tracking: Detailed graphs for PM2.5, PM10, and other gases.
Forecast Cards: A 7-day outlook to plan outdoor activities.
Health Tips: Dynamic advice based on current pollution levels.

📊 How it Works
Log in with the admin password.
Upload your air quality CSV file.
The system automatically cleans the data and calculates the AQI.
View the "Thermometer" and "Globe" indicators for a quick health check.
