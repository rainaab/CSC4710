# 🍍 Bikini Bottom Realty
### Find Your Dream Home Under the Sea!

**CSC4710 — Database Systems | Georgia State University | Fall 2026**

**Team Members:** Raina Bethea and Kyla Franklin

## Project Overview

Bikini Bottom Realty is a SpongeBob SquarePants-inspired real estate database management system developed using Python, 
SQLite, and Tkinter.

The project demonstrates relational database design, SQL querying, data integrity, transaction management, and database 
integration with Python through both command-line operations and an interactive graphical user interface (GUI).

The system uses fictional properties, agents, buyers, and sellers from the SpongeBob universe to simulate real estate 
listing and sales operations.

## Technologies Used

- **Python 3** — Database interaction and application logic
- **SQLite** — Relational database management
- **SQL** — Data retrieval, filtering, aggregation, and transactions
- **TKinter/ttk** — Interactive desktop dashboard
- **Pillow(PILL** — Property image processing and display
- **PyCharm** — Development environment
- **dbdiagram.io** — Relational schema visualization
- **GitHub** — Version control and collaboration

## Database Structure

The database contains six relational tables:

| Table | Description |
|---|---|
| Agent | Stores real estate agent information |
| Buyer | Stores potential property buyers |
| Seller | Stores property owners |
| Property | Stores property characteristics and image paths |
| Listing | Connects properties, sellers, agents, and listing prices |
| Sale | Records completed property transactions |

The populated demonstration database contains **145 records** across the six tables, including 40 properties, 40 listings, and 16 completed sales.

## SQL Queries and Operations

The project implements ten queries and database operations:

1. Available properties within a specified city and price range
2. Properties matching bedroom and pool requirements
3. Top-performing real estate agent by total sales
4. Agent sales performance, average prices, and listing-to-sale duration
5. Most expensive listed property with its associated image
6. Recording and verifying a completed property sale
7. Adding and verifying a new real estate agent
8. Properties priced above their city's average listing price
9. Completed sales ranked by buyer savings
10. Personalized property search based on buyer preferences
11. Longest-listed available residential properties
12. City market analysis of listing counts and prices

The queries demonstrate joins, filtering, aggregate functions, grouping, ordering, subqueries, and transaction operations.

## Interactive Dashboard
The project includes a Tkinter-based graphical interface in dashboard.py.
The dashboard contains three main sections:
### Find a Home
Allows users to search available residential properties using criteria such as:

- Preferred city
- Maximum budget
- Minimum bedrooms and bathrooms
- Swimming pool preference

Matching properties appear in a searchable results table. Selecting a property displays its address and associated image 
when available.

### City Market

Provides an overview of available residential real estate listings by city, including listing counts and pricing statistics.

### Longest Listed

Displays available residential properties ranked by the number of days they have been listed, using a selected reference date.

The dashboard retrieves information directly from the SQLite database and does not require modifying the underlying property 
records to perform searches.

## Project Files

| File or Folder | Purpose |
|---|---|
| `create_db.py` | Creates the database schema |
| `populate.py` | Populates the database with fictional records |
| `queries.py` | Executes the SQL queries |
| `dashboard.py` | Launches the interactive Tkinter dashboard |
| `record-sale.py` | Records a completed property transaction |
| `add_agent.py` | Inserts a new real estate agent |
| `add_images.py` | Associates property records with local images |
| `property_gallery.py` | Displays featured properties and images |
| `validate.py` | Checks database integrity and consistency |
| `real_estate.db` | Populated SQLite database |
| `images/` | Property image assets |
| `README.md` | Project documentation |

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rainaab/CSC4710.git
cd CSC4710
```

### 2. Verify Python Installation

Python 3 is required. Python 3.13 was used during final dashboard testing.

**macOS / Linux:**

```bash
python3 --version
```

**Windows:**

```powershell
py --version
```

Tkinter must also be available.

**macOS / Linux:**

```bash
python3 -m tkinter
```

**Windows:**

```powershell
py -m tkinter
```

A small demonstration window should appear if Tkinter is installed correctly.

### 3. Create a Virtual Environment

A virtual environment is recommended to keep project dependencies separate.

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Once activated, the virtual environment will be used for subsequent Python commands.

### 4. Install Required Dependencies

The dashboard uses Pillow for image processing.

```bash
python -m pip install Pillow
```

Alternatively, if a `requirements.txt` file is included:

```bash
python -m pip install -r requirements.txt
```

SQLite is included with standard Python installations through the built-in `sqlite3` module.

Verify SQLite support:

```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

The SQLite command-line application is optional.

### 5. Run the Interactive Dashboard

The repository includes a populated database, so recreating it is not necessary.

From the project directory, run:

```bash
python dashboard.py
```

The Bikini Bottom Realty desktop application should open with three tabs:

- Find a Home
- City Market
- Longest Listed

Use the dashboard to explore available properties, view property images, and analyze market information.

### 6. Run the SQL Queries

Execute the SQL queries and display their results in the terminal:

```bash
python queries.py
```

**Note:** Review the script before running it against the original database, since some project operations may modify records.

### 7. View the Property Gallery

Display featured properties and their images:

```bash
python property_gallery.py
```

### 8. Validate the Database

Execute the database validation procedures:

```bash
python validate.py
```

### 9. Database Modification Scripts

The project includes scripts that demonstrate database modifications:

```bash
python add_agent.py
python record-sale.py
```

**Important:** These scripts may change database records. Create a backup before testing modifications.

Avoid rerunning `create_db.py` or `populate.py` against the provided populated database without reviewing their effects.

## Data Integrity and Validation

The project includes validation procedures to verify:

- Database table record counts
- Foreign key integrity
- Overall SQLite database integrity
- Consistency between listings and completed sales
- Valid sale and listing dates
- Absence of duplicate property addresses

All six validation checks passed during development.

## Property Images

Featured properties include local image files representing recognizable homes and locations from the SpongeBob universe.

Images are stored in the `images/` directory, with their relative paths referenced in the database.

The interactive dashboard uses Pillow to load images and resize them proportionally to fit the preview area without stretching.

Properties without a valid associated image may display a placeholder message.

For image previews to work correctly, keep the `images/` folder in the project directory and preserve the filenames referenced by the database.

## Troubleshooting

### Dashboard Does Not Open

Verify that Python supports Tkinter:

```bash
python -m tkinter
```

If Tkinter is unavailable, install a Python distribution that includes a compatible Tcl/Tk installation.

### Pillow Import Error

Install Pillow into the active Python environment:

```bash
python -m pip install Pillow
```

### Property Images Are Missing

Confirm that the `images/` directory exists and contains the files referenced by the database.
Run the application from the project directory.

### Database File Cannot Be Found

Confirm that `real_estate.db` exists in the expected project location.
Avoid recreating or overwriting the provided database unless necessary.

### Using PyCharm

Open the cloned project folder and configure the project interpreter to use the virtual environment created during setup.
Run `dashboard.py` to launch the graphical interface.

## Project Purpose

This project applies core relational database concepts to a creative, fictional real estate scenario.
It demonstrates how structured data can support property searches, transaction tra