import pymysql
import pandas as pd
from sqlalchemy import create_engine
# ==============================
# STEP 1: LOAD CSV DATA
# ==============================
print("Loading cleaned earthquake data...")
df = pd.read_csv(r"C:\Users\Niresh\Guvi\earthquake_CLEAN(2019 to 2026.).csv")
print(f"Loaded {len(df)} records\n")

# ==============================
# STEP 2: CREATE DATABASE ENGINE
# ==============================
print("Connecting to MySQL...")
engine = create_engine(
    "mysql+pymysql://root:12345@localhost/Project"
)
print("Connected to MySQL\n")

# ==============================
# STEP 3: INSERT DATA
# ==============================
print("Inserting data into Earthquake table...")
try:
    df.to_sql(
        name="Earthquake",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000
    )
    print("Data inserted successfully\n")
except Exception as e:
    print("Error inserting data:", e)

# ==============================
