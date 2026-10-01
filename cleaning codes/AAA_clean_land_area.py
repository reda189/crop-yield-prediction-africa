import pandas as pd

# ==========================================
# Clean World Bank Land Area Data
# Input  : M2C1_landareadata.csv
# Output : M2C1_cleaned_land_area.csv
# ==========================================

INPUT_FILE = "M2C1_agricultural_land_data.csv"
OUTPUT_FILE = "M2C1_cleaned_land_area.csv"
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

df = df.dropna(how="all")

id_cols = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
year_cols = [str(y) for y in range(2000, 2023)]
df = df[id_cols + year_cols].copy()

df = df[df["Country Name"].isin(AFRICAN_COUNTRIES)].copy()

df = df.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=year_cols,
    var_name="Year",
    value_name="Land_Area"
)

df.rename(columns={"Country Name": "Country"}, inplace=True)

df = df.dropna(subset=["Land_Area"])

df["Year"] = df["Year"].astype(int)
df["Land_Area"] = pd.to_numeric(df["Land_Area"], errors="coerce")
df = df.dropna(subset=["Land_Area"])

df = df[["Country", "Country Code", "Year", "Land_Area"]].reset_index(drop=True)

df.to_csv(OUTPUT_FILE, index=False)

print("Saved:", OUTPUT_FILE)
print(df.head())
print("Shape:", df.shape)
print("Years:", df["Year"].min(), "to", df["Year"].max())
print("Countries:", df["Country"].nunique())