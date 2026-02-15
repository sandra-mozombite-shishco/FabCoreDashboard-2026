# %% [markdown]
# # FabCore Dashboard Data Processing
# This script merges operation, user, and course databases to generate KPIs.

# %% Libraries
import pandas as pd
import os
import numpy as np

# 1. PORTABLE PATH SETUP
try:
    base_path = os.path.dirname(os.path.abspath(__file__))
except NameError:
    base_path = os.getcwd()

# If your data is in a folder named 'data' relative to the script
data_dir = os.path.abspath(os.path.join(base_path, '..', 'data'))

# %%
# 2. LOAD DATA
# Using semicolon as delimiter based on your file structure
df_operation = pd.read_csv(os.path.join(data_dir, 'PythonTest_RegistroUso.csv'), sep=';')
df_users = pd.read_csv(os.path.join(data_dir, 'PythonTest_Usuarios.csv'), sep=';', encoding='latin-1')
df_courses = pd.read_csv(os.path.join(data_dir, 'PythonTest_CursosPUCP.csv'), sep=';', encoding='latin-1')

df_operation.columns = df_operation.columns.str.strip()
df_courses.columns = df_courses.columns.str.strip()
df_users.columns = df_users.columns.str.strip()
# Quick look at the raw data in the Interactive Window
print("Raw operation Data:")
display(df_operation.head()) 
display(df_users.head()) 
display(df_courses.head())

# %%
# 3. CLEANING, MAPPING, AND JOINS
# Convert timestamp
df_operation['Timestamp'] = pd.to_datetime(df_operation['Timestamp'], dayfirst=True)

# Extract date and hour
df_operation['Date'] = df_operation['Timestamp'].dt.date
df_operation['Hour'] = df_operation['Timestamp'].dt.time

# Convert duration (minutes → timedelta)
df_operation['Duration'] = pd.to_timedelta(df_operation['UseTime'], unit='m')

# Accurate decimal hours
## df_operation['Hours'] = df_operation['Duration'].dt.total_seconds() / 3600

# Mapping Staff to Nodes
node_map = {'Diego': 'FabCore 1', 'Ernesto': 'FabCore 2', 'Mariela': 'FabCore 3'}
df_operation['FabCore Nodo'] = df_operation['FabCore Staff'].map(node_map)

# MASTER JOIN
# Merging operation with users to get Career and with courses to get Course Names
df_master = pd.merge(df_operation, df_users[['DNI', 'Carrera']], on='DNI', how='left')
df_master = pd.merge(df_master, df_courses[['CODIGO', 'NOMBRE']], left_on='Course', right_on='CODIGO', how='left')

# Cleaning, renaming and sort columns for clarity
df_master = df_master.drop(columns=['CODIGO'])
df_master = df_master.rename(columns={'NOMBRE': 'Nombre Curso'})

df_master = df_master.rename(columns={
    'Date': 'Dia',
    'Hour': 'Hora',
    'Code': 'Codigo PUCP',
    'FabCore Staff': 'FabCore staff',
    'Service': 'Servicio',
    'UseTime': 'Tiempo uso',
    'Grams': 'Gramos',
    'Duration': 'Duracion',
    'Machine': 'Equipo',
    'Course': 'Codigo curso',
    'Nombre Curso': 'Nombre curso'
})

df_master = df_master[[
    'Timestamp',
    'Dia',
    'Hora',
    'DNI',
    'Codigo PUCP',
    'FabCore Nodo',
    'FabCore staff',
    'Servicio',
    'Tiempo uso',
    'Gramos',
    'Duracion',
    'Equipo',
    'Codigo curso',
    'Nombre curso',
    'Carrera'
]]

# Preview the joined Master Table
print("Joined Master Table:")
display(df_master.head())


# %%
# 4. METRIC GENERATION: Machine Hours
df_master['Year'] = df_master['Timestamp'].dt.year
df_master['Week'] = df_master['Timestamp'].dt.isocalendar().week

# Total accumulated Hours in the Year
total_yearly_hours = df_master.groupby('Year')['Duracion'].sum()
print(f"Total Yearly Hours: \n{total_yearly_hours}")

# Weekly machine hours per Node
weekly_hours = df_master.groupby(['Year', 'Week', 'FabCore Nodo'])['Duracion'].sum().reset_index()
display(weekly_hours.head())

# %%
# 5. METRIC GENERATION: Career Percentages
# % Students served per career vs Total potential students
students_served = df_master.groupby('Carrera')['DNI'].nunique()
total_students = df_users.groupby('Carrera')['DNI'].nunique()
career_reach = (students_served / total_students).fillna(0) * 100

# % Total Attentions per career
attentions_share = df_master['Carrera'].value_counts(normalize=True) * 100

print("Career Reach (% of their total population):")
display(career_reach)

# %%
# 6. METRIC GENERATION: Course Frequency per Node
course_perf = df_master.groupby(['FabCore Nodo', 'Nombre curso']).size().reset_index(name='Frequency')

print("Course Frequency per FabCore Node:")
display(course_perf.sort_values(by='Frequency', ascending=False))

# %%
# 7. EXPORT DATA FOR QUARTO
output_path = os.path.join(data_dir, 'Processed_Dashboard_Data.csv')
df_master.to_csv(output_path, index=False)
print(f"Successfully exported cleaned data to: {output_path}")
# %%
