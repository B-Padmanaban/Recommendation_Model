import pandas as pd
import re
import os
import sys

# Use absolute path for the CSV file
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "SCHEMEDATA.csv")

# Load and clean data on module load (once)
try:
    df = pd.read_csv(csv_path)
    df = df.dropna(axis=1, how="all")
    df.columns = df.columns.str.strip().str.upper()
    income_column = "INCOME" if "INCOME" in df.columns else "ANNUAL INCOME"
    # Print to stderr instead of stdout
    print(f"Successfully Fetched Recommended Schemes",file=sys.stderr)
except Exception as e:
    # Print to stderr instead of stdout
    print(f"Error Fetching Recommended Schemes",file=sys.stderr)
    # Create an empty DataFrame as fallback
    df = pd.DataFrame()

def is_numeric(value):
    return bool(re.match(r"^\d+$", str(value)))

def is_within_range(user_value, scheme_value):
    scheme_value = str(scheme_value).strip()

    if not any(char.isdigit() for char in scheme_value):
        return str(user_value).lower() == scheme_value.lower()

    if match := re.match(r"([<>]=?)\s*(\d+)", scheme_value):
        operator, number = match.groups()
        number = int(number)
        return eval(f"{user_value} {operator} {number}")

    elif "-" in scheme_value:
        parts = scheme_value.split("-")
        if len(parts) == 2 and all(is_numeric(p.strip()) for p in parts):
            lower, upper = map(int, parts)
            return lower <= user_value <= upper

    return str(user_value).lower() == scheme_value.lower()

def recommend_schemes(user_profile: dict):
    if not isinstance(df, pd.DataFrame) or df.empty:
        # Print to stderr instead of stdout
        print("DataFrame is empty or invalid", file=sys.stderr)
        return []
        
    user_profile = {key.upper(): value for key, value in user_profile.items()}
    if "CATEGORY" not in user_profile:
        return []

    filtered_schemes = df[df["CATEGORY"].str.contains(user_profile["CATEGORY"], case=False, na=False)]
    recommendations = []

    for _, scheme in filtered_schemes.iterrows():
        matched_attributes = []
        unmatched_attributes = []
        total_non_empty_attributes = 0
        total_matched_attributes = 0

        for attribute, user_value in user_profile.items():
            column_name = attribute.upper()

            if column_name == "CATEGORY" or column_name not in scheme:
                continue

            if pd.notna(scheme[column_name]) and str(scheme[column_name]).strip():
                total_non_empty_attributes += 1
                scheme_values = str(scheme[column_name]).split(", ")

                if any(is_within_range(user_value, value) for value in scheme_values):
                    matched_attributes.append(column_name)
                    total_matched_attributes += 1
                else:
                    unmatched_attributes.append(column_name)

        if total_matched_attributes == total_non_empty_attributes:
            recommendations.append({
                "Scheme Name": scheme["SCHEME NAME"],
                "Matched Attributes": matched_attributes,
                "Unmatched Attributes": unmatched_attributes
            })

    return recommendations