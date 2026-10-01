import pandas as pd

# ==========================================
# Clean Temperature Data
# Input  : M2C1_temperature_data.csv
# Output : M2C1_cleaned_temperature.csv
# ==========================================

INPUT_FILE = "M2C1_temperature_data.csv"
OUTPUT_FILE = "M2C1_cleaned_temperature.csv"

AFRICAN_COUNTRY_CODES = [
    "DZA","AGO","BEN","BWA","BFA","BDI","CPV","CMR","CAF","TCD","COM",
    "COG","CIV","COD","DJI","EGY","GNQ","ERI","SWZ","ETH","GAB","GMB",
    "GHA","GIN","GNB","KEN","LSO","LBR","LBY","MDG","MWI","MLI","MRT",
    "MUS","MAR","MOZ","NAM","NER","NGA","RWA","STP","SEN","SYC","SLE",
    "SOM","ZAF","SSD","SDN","TGO","TUN","UGA","TZA","ZMB","ZWE"
]

df = pd.read_csv(INPUT_FILE)

# Keep only useful columns
df = df[["REF_AREA", "REF_AREA_LABEL", "TIME_PERIOD", "OBS_VALUE", "INDICATOR_LABEL", "UNIT_MEASURE_LABEL"]].copy()

# Keep only African countries
df = df[df["REF_AREA"].isin(AFRICAN_COUNTRY_CODES)].copy()

# Keep only years 2000-2022
df = df[(df["TIME_PERIOD"] >= 2000) & (df["TIME_PERIOD"] <= 2022)].copy()

# Rename columns
df.rename(columns={
    "REF_AREA": "Country Code",
    "REF_AREA_LABEL": "Country",
    "TIME_PERIOD": "Year",
    "OBS_VALUE": "Temperature"
}, inplace=True)

# Remove missing values
df = df.dropna(subset=["Country", "Year", "Temperature"])

# Ensure numeric
df["Year"] = df["Year"].astype(int)
df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")
df = df.dropna(subset=["Temperature"])

# Keep only final useful columns
df = df[["Country", "Country Code", "Year", "Temperature"]].reset_index(drop=True)

# Save
df.to_csv(OUTPUT_FILE, index=False)

print("Saved:", OUTPUT_FILE)
print(df.head())
print("Shape:", df.shape)
print("Years:", df["Year"].min(), "to", df["Year"].max())
print("Countries:", df["Country"].nunique())