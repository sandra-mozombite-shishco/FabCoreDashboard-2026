import gspread
from google.oauth2.service_account import Credentials
import os
import json
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

#CREDS_FILE = 'credentials.json'
SPREADSHEET_ID = '1fSygIV3AmxzHOil6b-PgZ5_LO73nyrM87YrtL02rRuo'

# Authenticate
#creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(SPREADSHEET_ID)

# --- Read configuration sheet ---
try:
    config_ws = spreadsheet.worksheet("CONFIGURACION")
except gspread.WorksheetNotFound:
    raise Exception("Sheet 'CONFIGURACION' not found.")

# Get set of sheet names to read
config = config_ws.get_all_records()
sheets_to_read = set()
for row in config:
    name = row.get("NOMBRE_DE_HOJA")
    include = str(row.get("INCLUIR_DASHBOARD", "")).upper()
    if name and include == "TRUE":
        sheets_to_read.add(name)

# --- Load available sheets once ---
available_sheets = {ws.title: ws for ws in spreadsheet.worksheets()}

output = {}

for name in sheets_to_read:
    if name in available_sheets:
        output[name] = available_sheets[name].get_all_records()
    else:
        print(f"Warning: Sheet '{name}' not found.")

# --- Save JSON for GitHub Pages ---
Path("data").mkdir(parents=True, exist_ok=True)

with open("data/data.json", "w") as f:
    json.dump(output, f, indent=2)

print("Data updated successfully.")
