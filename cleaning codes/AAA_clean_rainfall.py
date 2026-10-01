import pandas as pd

# ==========================================
# Clean World Bank Rainfall Data
# Input  : M2C1_rainfalldata.csv
# Output : M2C1_cleaned_rainfall.csv
# ==========================================

INPUT_FILE = "M2C1_rainfall_data.csv"
OUTPUT_FILE = "M2C1_cleaned_rainfall.csv"

AFRICAN_COUNTRIES = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
    "Congo, Rep.", "Cote d'Ivoire", "Congo, Dem. Rep.", "Djibouti",
    "Egypt, Arab Rep.", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia",
    "Gabon", "Gambia, The", "Ghana", "Guinea", "Guinea-Bissau", "Kenya",
    "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali",
    "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia",
    "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal",
    "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan",
    "Sudan", "Togo", "Tunisia", "Uganda", "Tanzania", "Zambia", "Zimbabwe"
]

df = pd.read_csv(INPUT_FILE, skiprows=4)

# Remove empty rows
df = df.dropna(how="all")

# Keep identifier columns + years
id_cols = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
year_cols = [str(y) for y in range(2000, 2023)]
df = df[id_cols + year_cols].copy()

# Keep African countries only
df = df[df["Country Name"].isin(AFRICAN_COUNTRIES)].copy()

# Convert wide to long
df = df.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=year_cols,
    var_name="Year",
    value_name="Rainfall"
)

# Rename
df.rename(columns={"Country Name": "Country"}, inplace=True)

# Drop missing values
df = df.dropna(subset=["Rainfall"])

# Types
df["Year"] = df["Year"].astype(int)
df["Rainfall"] = pd.to_numeric(df["Rainfall"], errors="coerce")
df = df.dropna(subset=["Rainfall"])

# Reset index
df = df[["Country", "Country Code", "Year", "Rainfall"]].reset_index(drop=True)

# Save
df.to_csv(OUTPUT_FILE, index=False)

print("Saved:", OUTPUT_FILE)
print(df.head())
print("Shape:", df.shape)
print("Years:", df["Year"].min(), "to", df["Year"].max())
print("Countries:", df["Country"].nunique())