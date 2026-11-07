
import pandas as pd

input_file = "datasets/confirmed_planets.csv"
output_file = "datasets/confirmed_planets_working.csv"

df = pd.read_csv(input_file, comment="#", low_memory=False)

selected_columns = [
    "pl_name",
    "hostname",
    "discoverymethod",
    "disc_year",
    "pl_orbper",
    "pl_orbsmax",
    "pl_orbeccen",
    "pl_eqt",
    "pl_rade",
    "pl_bmasse",
    "pl_dens",
    "pl_insol",
    "st_teff",
    "st_mass",
    "st_rad",
    "st_age",
    "st_met",
    "st_logg",
    "sy_dist",
    "sy_vmag",
    "sy_tmag",
    "sy_pnum",
    "sy_snum"
]

available = [c for c in selected_columns if c in df.columns]

working_df = df[available].copy()
working_df.to_csv(output_file, index=False)

print("Original shape:", df.shape)
print("Working shape:", working_df.shape)
print("Saved to:", output_file)
