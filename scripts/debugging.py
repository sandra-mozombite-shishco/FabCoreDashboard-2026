from dataUse_construction import build_master_dataframe
from OperationMetrics_functions import total_students_served

# %%
df = build_master_dataframe()

df.head()

# %%
totalStOp=total_students_served(df)
totalStOp