# 🍍 Bikini Bottom Realty
### Find Your Dream Home Under the Sea!

**CSC4710 — Database Systems | Georgia State University | Fall 2026**

**Team Members:** Raina Bethea and Kyla Franklin

## Project Overview

Bikini Bottom Realty is a SpongeBob SquarePants-inspired real estate database management system developed using Python and SQLite.

The project demonstrates relational database design, SQL querying, data integrity, transaction management, and database integration with Python.

The system uses fictional properties, agents, buyers, and sellers from the SpongeBob universe to simulate real estate listing and sales operations.

## Technologies Used

- **Python 3** — Database interaction and application logic
- **SQLite** — Relational database management
- **SQL** — Data retrieval, filtering, aggregation, and transactions
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

The queries demonstrate joins, filtering, aggregate functions, grouping, ordering, subqueries, and transaction operations.

## Project Files

| File or Folder | Purpose |
|---|---|
| `create_db.py` | Creates the database schema |
| `populate.py` | Populates the database with fictional records |
| `queries.py` | Executes the SQL queries |
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

Python 3 is required.

```bash
python3 --version
```

### 3. SQLite Setup

SQLite is included with most standard Python installations through the built-in `sqlite3` module.

No separate Python package installation is typically required.

To verify SQLite support:

```bash
python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
```

The SQLite command-line application is optional and is not required to run the Python scripts.

### 4. Run the Project

The repository includes a populated database, so recreating it is not necessary.

To execute the SQL queries:

```bash
python3 queries.py
```

To display the featured property gallery:

```bash
python3 property_gallery.py
```

To validate the database:

```bash
python3 validate.py
```

The following scripts demonstrate database modifications:

```bash
python3 add_agent.py
python3 record-sale.py
```

**Note:** These scripts may change database records. Use a backup database when testing modifications, and avoid rerunning initialization or population scripts against the provided database without reviewing their effects.

## Data Integrity and Validation

The project includes validation procedures to verify:

- Database table record counts
- Foreign key integrity
- Overall SQLite database integrity
- Consistency between listings and completed sales
- Valid sale and listing dates
- Absence of duplicate property addresses

All six validation checks passed during development.

## Property Gallery

Eight featured properties include associated local image files, such as SpongeBob's pineapple house, Squidward's home, Patrick's rock, Sandy's treedome, Mr. Krabs' residence, and King Neptune's palace.

Images are stored locally in the `images/` directory, with their relative paths referenced in the database.

## Project Purpose

This project applies core relational database concepts to a creative, fictional real estate scenario. It demonstrates how structured data can support property searches, transaction tracking, sales analysis, and database integrity while maintaining a consistent and engaging theme.

*Bikini Bottom Realty — Where Every Home Is a Pineapple of Possibilities!* 🍍
