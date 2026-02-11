# FabCore Dashboard 2026

Interactive dashboard for managing academic manufacturing projects at FabCore Lab.

## Tech stack
- Quarto
- Python
- Git + GitHub

## Requirements
Before you start, download and extract these portable tools:

1. **Python 3.x** (pick one):
   - Option A: [WinPython](https://winpython.github.io/) - Recommended
   - Option B: System Python from [python.org](https://www.python.org)

2. **Git** - [Portable Git](https://git-scm.com/download/win)
   - Extract to: `D:\Portables\Git`

3. **Quarto** - [Download Quarto](https://quarto.org/docs/get-started/)
   - Extract to: `D:\Portables\Quarto-1.8.27-win`


## Setup (First Time Only)

1. **Clone the repository:**
   ```powershell
   git clone <your-repo-url>
   cd Dashboard2026
   ```

2. **Create virtual environment:**
   ```powershell
   python -m venv .venv
   ```

3. **Activate virtual environment:**
   ```powershell
   & .\.venv\Scripts\Activate.ps1
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

## How to run
1. Press `Ctrl + Shift + B` or click Preview (requieres Quarto extension for VS Code)

- Otherwise, for directly browser viewing:
    ```powershell 
    quarto preview index.qmd --to dashboard ```
## To Stop

Press `Ctrl + C` in the terminal
## Notes
- No admin permissions required (except for virtual environment if needed)
- Tools live in `D:\Portables`

## Workspace Settings

Portable tool paths are pre-configured in `.vscode/settings.json`

## Status
🚧 In development

## Author
Sandra Mozombite Shishco
(moshivuu)