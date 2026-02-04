AirAware – Smart Air Quality Prediction System

Problem Statement
Air pollution significantly affects public health and the environment. Predicting air quality levels in advance helps individuals and authorities take necessary preventive measures.

Objective
To predict air quality levels using machine learning techniques based on historical pollutant data.

Technologies Used
Language: Python
Data Handling: Pandas, NumPy
Visualization: Plotly, Matplotlib, Seaborn
Machine Learning: Scikit-learn
Web Framework: Streamlit

Dataset
The system processes air quality datasets containing parameters such as:
PM_{2.5} and PM_{10}
NO_2, SO_2, and CO

System Architecture
Input Data → Preprocessing → ML Model → AQI Prediction → Output Visualization

How to Run
Install dependencies:
pip install -r requirements.txt

Launch the dashboard:
streamlit run app.py

Future Scope
Real-time Prediction: Fetching live data from sensors.
API Integration: Connecting with weather forecasting services.
Mobile App: Developing a cross-platform mobile application for alerts.
