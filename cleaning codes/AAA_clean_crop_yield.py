import pandas as pd

# ==========================================
# Clean FAOSTAT Crop Yield Data
# Input  : FAOSTAT_data.csv
# Output : M2C1_cleaned_crop_yield.csv
# ==========================================

INPUT_FILE = "FAOSTAT_data.csv"
OUTPUT_FILE = "M2C1_cleaned_crop_yield.csv"

AFRICAN_COUNTRIES = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
    "Congo", "Côte d'Ivoire", "Democratic Republic of the Congo", "Djibouti",
    "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia",
    "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya",
    "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali",
    "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia",
    "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal",
    "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan",
    "Sudan", "Togo", "Tunisia", "Uganda", "United Republic of Tanzania",
    "Zambia", "Zimbabwe"
]

df = pd.read_csv(INPUT_FILE)

# Keep only useful columns
df = df[["Area", "Year", "Value", "Element"]].copy()

# Keep only Yield rows
df = df[df["Element"] == "Yield"].copy()

# Rename columns
df.rename(columns={
    "Area": "Country",
    "Year": "Year",
    "Value": "Crop_Yield"
}, inplace=True)

# Filter African countries
df = df[df["Country"].isin(AFRICAN_COUNTRIES)].copy()

# Filter years
df = df[(df["Year"] >= 2000) & (df["Year"] <= 2022)].copy()

# Remove missing values
df = df.dropna(subset=["Country", "Year", "Crop_Yield"])

# Ensure correct types
df["Year"] = df["Year"].astype(int)
df["Crop_Yield"] = pd.to_numeric(df["Crop_Yield"], errors="coerce")
df = df.dropna(subset=["Crop_Yield"])

# Reset index
df = df.reset_index(drop=True)

# Save cleaned file
df.to_csv(OUTPUT_FILE, index=False)

print("Saved:", OUTPUT_FILE)
print(df.head())
print("Shape:", df.shape)
print("Years:", df["Year"].min(), "to", df["Year"].max())
print("Countries:", df["Country"].nunique())