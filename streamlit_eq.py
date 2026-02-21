import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Earthquake Dashboard",
    layout="wide"
)

st.title("🌍 Earthquake Dashboard")

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
print("Connecting to MySQL...")
engine = create_engine(
    "mysql+pymysql://root:12345@localhost/Project"
)
print("Connected to MySQL\n")

# SQL TASKS (DROPDOWN)
# -------------------------------
TASKS = {
    "1.Top 10 - Strongest Earthquakes (magnitude)": {
        "query": """
            SELECT id, time, place, mag
            FROM Earthquake
            ORDER BY mag DESC
            LIMIT 10;
        """,
        "title": "Top 10 - Strongest Earthquakes (magnitude)"
    },

    "2.Top 10 - deepest earthquakes": {
        "query": """
            SELECT id, time, place, Depth_km
            FROM Earthquake
            ORDER BY Depth_km DESC
            LIMIT 10;
        """,
        "title": "Top 10 Deepest Earthquakes"
    },

    "3.Shallow High-Magnitude Earthquakes": {
        "query": """
            SELECT id, time, place, mag, Depth_km
            FROM Earthquake
            WHERE Depth_km < 50 AND mag > 7.5;
        """,
        "title": "Shallow High-Magnitude Earthquakes (<50km & mag >7.5)"
    },

    "5.Average magnitude per magType": {
        "query": """
            SELECT magType, AVG(mag) AS average_magnitude
            FROM Earthquake
            GROUP BY magType;
        """,
        "title": "Average Magnitude per magType"
    },

    "6.Year with Highest Earthquake Count": {
        "query": """
            SELECT YEAR(time) AS year, COUNT(*) AS earthquake_count
            FROM Earthquake
            GROUP BY YEAR(time)
            ORDER BY earthquake_count DESC
            LIMIT 5;
        """,
        "title": "Year with Highest Earthquake Count"
    },

    "7.Month with Highest Earthquake Count": {
        "query": """
            SELECT MONTHNAME(time) AS month, COUNT(*) AS earthquake_count
            FROM Earthquake
            GROUP BY MONTHNAME(time)
            ORDER BY earthquake_count DESC
            LIMIT 1;
        """,
        "title": "Month with Highest Earthquake Count"
    },

    "8.Most Earthquakes by Day of Week": {
        "query": """
            SELECT DAYNAME(time) AS day, COUNT(*) AS earthquake_count
            FROM Earthquake
            GROUP BY DAYNAME(time)
            ORDER BY earthquake_count DESC
            LIMIT 5;
        """,
        "title": "Most Earthquakes by Day of Week"
    },

    "9.Earthquakes by Hour of the Day": {
        "query": """
            SELECT HOUR(time) AS hour, COUNT(*) AS earthquake_count
            FROM Earthquake
            GROUP BY HOUR(time)
            ORDER BY hour;
        """,
        "title": "Earthquakes by Hour of the Day"
    },

    "10.Most Active Networks": {
        "query": """
            SELECT net, COUNT(*) AS earthquake_count
            FROM Earthquake
            GROUP BY net
            ORDER BY earthquake_count DESC
            LIMIT 5;
        """,
        "title": "Most Active Networks"
    },

    "11.Top 5 - Locations by Highest Casualties": {
        "query": """
            SELECT place, SUM(sig) AS total_impact
            FROM Earthquake
            GROUP BY place
            ORDER BY total_impact DESC
            LIMIT 5;
        """,
        "title": "Top 5 -  Locations by Highest Casualties"
    },

    "13.Average Economic Loss by Alert Level": {
        "query": """
            SELECT alert,  AVG(sig) AS avg_significance
            FROM Earthquake
            WHERE alert IS NOT NULL
            GROUP BY alert;
            ORDER BY avg_significance DESC
        """,
        "title": "Average Economic Loss by Alert Level"
    },

    "14.Reviewed vs automatic earthquakes": {
        "query": """
            SELECT status, COUNT(*) AS earthquake_count
            FROM Earthquake
            WHERE status IN ('reviewed','automatic')
            GROUP BY status;
        """,
        "title": "Reviewed vs Automatic Earthquakes"
    },

    "15.Earthquakes by type": {
        "query": """
            SELECT type, COUNT(*) AS earthquake_count
            FROM Earthquake
            GROUP BY type
            ORDER BY earthquake_count DESC;
        """,
        "title": "Earthquakes by Type"
    },

    "16.Earthquakes by data type": {
        "query": """
            SELECT types, COUNT(*) AS earthquake_count
            FROM Earthquake
            GROUP BY types
            ORDER BY earthquake_count DESC;
        """,
        "title": "Earthquakes by Data Source"
    },

    "18.High station coverage events (nst > 50)": {
        "query": """
            SELECT id, time, place, nst
            FROM Earthquake
            WHERE nst > 50
            ORDER BY nst DESC;
        """,
        "title": "High Station Coverage Events"
    },
    "19.Number of tsunamis triggered per year":{
        "query": """
            SELECT YEAR(time) AS year, COUNT(*) AS tsunami_count
            FROM Earthquake
            WHERE tsunami = 1
            GROUP BY YEAR(time)
            ORDER BY year;
        """,
        "title": "Tsunamis Triggered per Year"
    },
    "20.Count earthquakes by alert levels":{
        "query": """
            SELECT alert, COUNT(*) AS earthquake_count
            FROM Earthquake
            WHERE alert IN ('red', 'orange', 'green', 'yellow')
            GROUP BY alert
            ORDER BY earthquake_count DESC;
        """,
        "title": "Earthquakes by Alert Levels"
    },
    "21.Top 5 - Countries by Average Earthquake Magnitude (Last 5 Years)":{
        "query": """
            SELECT country,AVG(mag) AS avg_magnitude 
            FROM Earthquake
            WHERE YEAR(time) >= YEAR(CURDATE()) - 5
            GROUP BY country
            ORDER BY avg_magnitude DESC
            LIMIT 5;
        """,
        "title": "Top 5 - Countries by Average Earthquake Magnitude (Last 10 Years))"
    },
     "22.Countries with Both Shallow and Deep Earthquakes in the Same Month":{  
         "query":"""
              SELECT country, YEAR(time) AS year, MONTH(time) AS month
              FROM Earthquake
              GROUP BY country, YEAR(time), MONTH(time)
              HAVING
              SUM(CASE WHEN depth_km < 70 THEN 1 ELSE 0 END) > 0 
              AND
              SUM(CASE WHEN depth_km >= 300 THEN 1 ELSE 0 END) > 0;    
              """,
        "title": "Countries with Both Shallow and Deep Earthquakes in the Same Month"
    },
     "25.Earthquake Depth Analysis Within ±5° of the Equator":{
        "query" : """
            SELECT country, AVG(Depth_km) AS avg_depth
            FROM Earthquake
            WHERE latitude BETWEEN -5 AND 5
            GROUP BY country;
            """,
        "title": "Earthquake Depth Analysis Within ±5° of the Equator"
    }, 
    "27.Average Magnitude Difference: Tsunami vs Non-Tsunami Earthquakes":{
        "query": """
            SELECT 
            ROUND(
            (SELECT AVG(mag) FROM Earthquake WHERE tsunami = 1) -
            (SELECT AVG(mag) FROM Earthquake WHERE tsunami = 0),
            2) AS magnitude_difference;
            """,
            "title": "Average Magnitude Difference: Tsunami vs Non-Tsunami Earthquakes"
    },
    "28.Average Error Margin of Earthquakes by Gap and RMS":{
        "query": """
            SELECT gap,rms,
            ROUND((gap + rms) / 2, 2) AS average_error_margin
           FROM Earthquake
           ORDER BY average_error_margin DESC
           LIMIT 10;
           """,
           "title": "Average Error Margin of Earthquakes by Gap and RMS"
    },
     "30.Regions with Most Deep Earthquakes (Depth > 300 km)":{   
        "query" : """
        SELECT 
        region,
        COUNT(*) AS deep_earthquake_count
        FROM Earthquake
        WHERE depth > 300
        GROUP BY region
        ORDER BY deep_earthquake_count DESC;
        """,
        "title": "Regions with Most Deep Earthquakes (Depth > 300 km)"
    },   }
    

# -------------------------------
# DROPDOWN
# -------------------------------
selected_task = st.selectbox(
    "📊 Select Analyst Task",
    list(TASKS.keys())
)

# -------------------------------
# RUN QUERY & DISPLAY
# -------------------------------
if st.button("Run"):
    try:
        query = TASKS[selected_task]["query"]
        title = TASKS[selected_task]["title"]

        df = pd.read_sql(query, engine)

        st.subheader(title)
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Database error: {e}")
        