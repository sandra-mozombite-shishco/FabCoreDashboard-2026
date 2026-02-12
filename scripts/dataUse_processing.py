# %% [markdown]
## Current Working Directory
import os
print(os.getcwd())

# %% [markdown]
# # Cell 1: Setup and Functions
# This is a Markdown cell (starts with # %% [markdown]). 
# It's for your notes, not for code!

import pandas as pd
import os

def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)
    metrics = {
        "total_hours": df['UseTime'].sum() / 60,
        "total_grams": df['Grams'].sum(),
        "unique_users": df['Name'].nunique()
    }
    return df, metrics

# %% 
# Cell 2: Execution and Inspection
# This is a regular Code cell.

base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, '..', 'data', 'FabCore_Usage_Data_Expanded.csv')

# Only this part runs when you click "Run Cell" here
df_cleaned, kpis = load_and_clean_data(file_path)
print(f"Data loaded! KPIs: {kpis}")

# %%
# Cell 3: Data Viewer
# Run this to see the table in the Interactive Window
df_cleaned.head()

# %% [markdown]
# # Data Processing Inspection

import pandas as pd

# Reading and organizing data, calculating KPIs, and preparing for visualization in Quarto.
def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], dayfirst=True)
    
    # KPIs
    metrics = {
        "total_hours": df['UseTime'].sum() / 60,
        "total_grams": df['Grams'].sum(),
        "unique_users": df['Name'].nunique()
    }
    return df, metrics
