import requests
from datetime import datetime
import pandas as pd


BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def month_(start_year, end_year):
    records = []

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            start_date = datetime(year, month, 1)

            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)

            params = {
                "format": "geojson",
                "starttime": start_date.strftime("%Y-%m-%d"),
                "endtime": end_date.strftime("%Y-%m-%d"),
                "minmagnitude": 3.0
            }

            response = requests.get(BASE_URL, params=params)

            if response.status_code != 200:
                print(f"Failed for {params['starttime']}")
                continue

            data = response.json()
            features = data.get("features", [])

            for f in features:
                props = f.get("properties", {})
                geom = f.get("geometry", {})
                coordinates = geom.get("coordinates", [None, None, None])

                record = {
                    "id": f.get("id"),
                    "time": pd.to_datetime(props.get("time"), unit="ms", errors="coerce"),
                    "updated": pd.to_datetime(props.get("updated"), unit="ms", errors="coerce"),
                    "Longitude": coordinates[0],
                    "Latitude": coordinates[1],
                    "Depth_km": coordinates[2],
                    "mag": props.get("mag"),
                    "magType": props.get("magType"),
                    "place": props.get("place"),
                    "status": props.get("status"),
                    "tsunami": props.get("tsunami"),
                    "alert": props.get("alert"),
                    "felt": props.get("felt"),
                    "cdi": props.get("cdi"),
                    "mmi": props.get("mmi"),
                    "sig": props.get("sig"),
                    "net": props.get("net"),
                    "code": props.get("code"),
                    "ids": props.get("ids"),
                    "sources": props.get("sources"),
                    "types": props.get("types"),
                    "nst": props.get("nst"),
                    "dmin": props.get("dmin"),
                    "rms": props.get("rms"),
                    "gap": props.get("gap"),
                    "type": props.get("type")
                }
                records.append(record)

    return pd.DataFrame(records)
    
df = month_(2019, 2026)

# ---- RUN PROGRAM ----
# Extract country using Regex
df["country"] = df["place"].str.extract(r",\s*([^,]+)$")

# String Cleaning
print("STRING CLEANING:")
string_cols = ["magType", "status", "type", "net", "alert", "place", "sources", "types", "ids"]

for col in string_cols:
    if col in df.columns:
        # Remove leading/trailing commas and quotes, then lowercase and strip
        df[col] = df[col].astype(str).str.replace('^"|"$', '', regex=True).str.replace('^,|,$', '', regex=True).str.lower().str.strip()
        # Replace empty strings or 'nan' with mode
        #Fill with median if there are any NaN values
        #This selects one column from the DataFrame./
        # isna() checks for NaN values and returns a boolean Series
        # ./any() checks if any value in the Series is True.
        df[col] = df[col].replace(['nan', '', 'none'], pd.NA)
        if df[col].isna().any() and len(df[col].dropna()) > 0:
            df[col] = df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'unknown')
        print(f"  {col}")


# ===== NUMERIC CLEANING =====
print("\nNUMERIC CLEANING:")
numeric_cols = ["mag", "Longitude", "Latitude", "Depth_km", "nst", "dmin", "rms", "gap", "magError", "depthError", "magNst", "sig"]
for col in numeric_cols:
    if col in df.columns:
        #Converts valid numbers → numeric/Invalid values → converted to NaN/Changes dtype to float
        df[col] = pd.to_numeric(df[col], errors='coerce')
        #Fill with median if there are any NaN values
        #This selects one column from the DataFrame./
        # isna() checks for NaN values and returns a boolean Series
        # ./any() checks if any value in the Series is True.
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())
        print(f"   {col}")



# Save
#df.to_csv("earthquake_CLEAN(2019 to 2026.).csv", index=False)
df.to_json("earthquake_CLEAN(2019_2026).json", orient="records", date_format="iso")
#print(f"\n Saved: earthquake_CLEAN(2019 to 2026).csv")
print(f"\n Saved:earthquake_CLEAN(2019_2026).json ")

#print("Total records:", df.shape)
#print(df.head())
#print(df.tail())
#print(df.dtypes)
#print(df.alert.unique)















