import pandas as pd

# ==========================================
# Clean World Bank Fertilizer Data
# Input  : M2C1_fertilizerdata.csv
# Output : M2C1_cleaned_fertilizer.csv
# ==========================================

INPUT_FILE = "M2C1_fertilizer_consumption_data.csv"
OUTPUT_FILE = "M2C1_cleaned_fertilizer.csv"

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
    value_name="Fertilizer_Usage"
)

df.rename(columns={"Country Name": "Country"}, inplace=True)

df = df.dropna(subset=["Fertilizer_Usage"])

df["Year"] = df["Year"].astype(int)
df["Fertilizer_Usage"] = pd.to_numeric(df["Fertilizer_Usage"], errors="coerce")
df = df.dropna(subset=["Fertilizer_Usage"])

df = df[["Country", "Country Code", "Year", "Fertilizer_Usage"]].reset_index(drop=True)

df.to_csv(OUTPUT_FILE, index=False)

print("Saved:", OUTPUT_FILE)
print(df.head())
print("Shape:", df.shape)
print("Years:", df["Year"].min(), "to", df["Year"].max())
print("Countries:", df["Country"].nunique())