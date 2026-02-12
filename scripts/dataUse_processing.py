# %% [markdown]
# ## Setup and Libraries
import os
import pandas as pd

# %% 
# Cell 1: Functions
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
# Cell 2: Execution and Pathing
import os # Importing AGAIN here just to be 100% safe for Quarto
import pandas as pd

try:
    # Works when running the .py file directly
    base_path = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Works when Quarto/Jupyter runs the file
    base_path = os.getcwd()

# Build path: we use '..' because your script is in /scripts and data is in /data
file_path = os.path.join(base_path, '..', 'data', 'FabCore_Usage_Data_Expanded.csv')

print(f"Attempting to load: {file_path}")
df_cleaned, kpis = load_and_clean_data(file_path)
print(f"Data loaded! KPIs: {kpis}")

# %%
# Cell 3: Data Viewer
df_cleaned.head()