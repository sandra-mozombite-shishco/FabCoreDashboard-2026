'''# %% [markdown]
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

# Generate fab_id for users, just for quick identification in the dashboard (not used for joins)
df_users.insert(
    0,  # posición 0 = primera columna
    "fab_id",
    [f"FabUser2026-{str(i+1).zfill(5)}" for i in range(len(df_users))]
)

# Join fab_id to operation for easier tracking in the dashboard
df_operation = pd.merge(df_operation, df_users[['DNI', 'fab_id']], on='DNI', how='left')


# Delete leading/trailing spaces from column names
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

# Mapping agreements courses
course_agreements = {'SI': 'Convenio','NO': 'Sin convenio'} # A course without "convenio" implies that the student will use their subvention or their own material"
df_operation['Convenio material'] = df_operation['FabCore Staff'].map(node_map)

# MASTER JOIN
# Merging operation with users to get Career and with courses to get Course Names
df_master = pd.merge(df_operation, df_users[['DNI', 'Carrera']], on='DNI', how='left')
df_master = pd.merge(df_master, df_courses[['CODIGO', 'NOMBRE', 'CONVENIO']], left_on='Course', right_on='CODIGO', how='left')
df_master['Convenio curso'] = df_master['CONVENIO'].map(course_agreements)

# Cleaning, renaming and sort columns for clarity
#df_master = df_master.drop(columns=['CODIGO', 'DNI', 'Code', 'Name','CONVENIO'])

df_master = df_master.rename(columns={
    'Date': 'Dia',
    'Hour': 'Hora',
    'fab_id': 'Usuario FAB',
    'FabCore Staff': 'FabCore staff',
    'Service': 'Servicio',
    'UseTime': 'Tiempo uso',
    'Grams': 'Gramos',
    'Duration': 'Duracion',
    'Machine': 'Equipo',
    'Course': 'Codigo curso',
    'NOMBRE': 'Nombre curso'
})

df_master = df_master[[
    'Timestamp',
    'Dia',
    'Hora',
    'Usuario FAB',
    'Carrera',
    'FabCore Nodo',
    'FabCore staff',
    'Servicio',
    'Tiempo uso',
    'Gramos',
    'Duracion',
    'Equipo',
    'Codigo curso',
    'Nombre curso',
    'Convenio material',
    'Tipo de Servicio'
]]

# Preview the joined Master Table
print("Joined Master Table:")
df_master.head()

# %%
# 4. EXPORT DATA FOR QUARTO
output_path = os.path.join(data_dir, 'Processed_RegisterOperation.csv')
df_master.to_csv(output_path, index=False)
print(f"Successfully exported cleaned data to: {output_path}")
# %%





# %%
# 5. METRIC GENERATION: Machine Hours
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

'''
"""
FabCore Dashboard - Data Construction Pipeline
Builds master dataset and generates core metrics.

Can be:
- Imported as a module
- Executed as standalone script
"""

import pandas as pd
import os
from datetime import datetime


# ============================================================
# 1. PATH SETUP
# ============================================================

def get_data_directory():
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_path = os.getcwd()

    return os.path.abspath(os.path.join(base_path, '..', 'data'))


# ============================================================
# 2. LOAD DATA
# ============================================================

def load_raw_data(data_dir):
    df_operation = pd.read_csv(
        os.path.join(data_dir, 'PythonTest_RegistroUso.csv'),
        sep=';'
    )

    df_users = pd.read_csv(
        os.path.join(data_dir, 'PythonTest_Usuarios.csv'),
        sep=';',
        encoding='latin-1'
    )

    df_courses = pd.read_csv(
        os.path.join(data_dir, 'PythonTest_CursosPUCP.csv'),
        sep=';',
        encoding='latin-1'
    )

    # Clean column names
    df_operation.columns = df_operation.columns.str.strip()
    df_users.columns = df_users.columns.str.strip()
    df_courses.columns = df_courses.columns.str.strip()

    return df_operation, df_users, df_courses


# ============================================================
# 3. USER ID GENERATION
# ============================================================

def generate_user_ids(df_users):
    year = datetime.now().year

    df_users = df_users.copy()

    df_users.insert(
        0,
        "fab_id",
        [f"FabUser{year}-{str(i+1).zfill(5)}" for i in range(len(df_users))]
    )

    return df_users


# ============================================================
# 4. MASTER DATAFRAME CONSTRUCTION
# ============================================================

def build_master_dataframe():
    data_dir = get_data_directory()

    df_operation, df_users, df_courses = load_raw_data(data_dir)

    df_users = generate_user_ids(df_users)

    # Join fab_id into operation
    df_operation = pd.merge(
        df_operation,
        df_users[['DNI', 'fab_id', 'Tipo de usuario']],
        on='DNI',
        how='left'
    )

    # Convert timestamp
    df_operation['Timestamp'] = pd.to_datetime(
        df_operation['Timestamp'],
        dayfirst=True
    )

    # Spanish mappings
    meses_spa = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    dias_spa = {
    "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
    "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
    }

    # Añadir columna de semestreeeeee jajaja D:

    df_operation['Date'] = df_operation['Timestamp'].dt.date
    df_operation['Hour'] = df_operation['Timestamp'].dt.time
    df_operation['Año'] = df_operation['Timestamp'].dt.year
    df_operation['Mes'] = df_operation['Timestamp'].dt.month.map(meses_spa)
    df_operation['Semana'] = df_operation['Timestamp'].dt.isocalendar().week
    df_operation['Día'] = df_operation['Timestamp'].dt.day_name().map(dias_spa)

    df_operation['Duration'] = pd.to_timedelta(
        df_operation['UseTime'],
        unit='m'
    )

    # Mapping staff to nodes
    node_map = {
        'Diego': 'FabCore 1',
        'Ernesto': 'FabCore 2',
        'Mariela': 'FabCore 3'
    }

    df_operation['FabCore Nodo'] = df_operation['FabCore Staff'].map(node_map)

    # Course agreement mapping
    course_agreements = {
        'SI': 'Convenio',
        'NO': 'Sin convenio'
    }

    # MASTER JOIN
    df_master = pd.merge(
        df_operation,
        df_users[['DNI', 'Carrera']],
        on='DNI',
        how='left'
    )

    df_master = pd.merge(
        df_master,
        df_courses[['CODIGO', 'NOMBRE', 'CONVENIO']],
        left_on='Course',
        right_on='CODIGO',
        how='left'
    )

    df_master['Convenio curso'] = df_master['CONVENIO'].map(course_agreements)

    # Rename columns
    df_master = df_master.rename(columns={
        'Date': 'Fecha',
        'Hour': 'Hora',
        'fab_id': 'Usuario FAB',
        'FabCore Staff': 'FabCore staff',
        'Service': 'Servicio',
        'UseTime': 'Tiempo uso',
        'Grams': 'Gramos',
        'Duration': 'Duracion',
        'Machine': 'Equipo',
        'Course': 'Codigo curso',
        'NOMBRE': 'Nombre curso'
    })

    df_master = df_master[[
        'Timestamp',
        'Fecha',
        'Hora',
        'Año',
        'Mes',
        'Día',
        'Semana',
        'Usuario FAB',
        'Tipo de usuario',
        'Carrera',
        'FabCore Nodo',
        'FabCore staff',
        'Servicio',
        'Tiempo uso',
        'Gramos',
        'Duracion',
        'Equipo',
        'Codigo curso',
        'Nombre curso',
        'Convenio curso',
        'Tipo de Servicio'
    ]]

    return df_master


'''# ============================================================
# 5. METRIC GENERATION
# ============================================================

def compute_machine_metrics(df_master):
    df = df_master.copy()

    df['Year'] = df['Timestamp'].dt.year
    df['Week'] = df['Timestamp'].dt.isocalendar().week

    total_yearly_hours = df.groupby('Year')['Duracion'].sum()

    weekly_hours = (
        df.groupby(['Year', 'Week', 'FabCore Nodo'])['Duracion']
        .sum()
        .reset_index()
    )

    return total_yearly_hours, weekly_hours'''

# ============================================================
# 5. EXPORT
# ============================================================

def export_master(df_master):
    data_dir = get_data_directory()
    output_path = os.path.join(data_dir, 'Processed_RegisterOperation.csv')

    df_master.to_csv(output_path, index=False)
    print(f"✔ Successfully exported cleaned data to: {output_path}")


# ============================================================
# 6. SCRIPT EXECUTION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    print("🔄 Building FabCore master dataset...")

    df_master = build_master_dataframe()
    export_master(df_master)

    print("✅ Pipeline completed successfully.")