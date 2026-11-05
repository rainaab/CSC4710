# 🍍 Bikini Bottom Realty
### Find Your Dream Home Under the Sea!

**A Real Estate Database Management System**

Bikini Bottom Realty is a fictional real estate database management system inspired by *SpongeBob SquarePants*. Developed for Georgia State University's Database Systems course, this project demonstrates relational database design, SQL querying, transaction management, data validation, and graphical user interface development using Python and SQLite.

The system manages real estate agents, buyers, sellers, properties, listings, and completed transactions across Bikini Bottom and surrounding neighborhoods.

---

## 🛠️ Technologies Used

- **Python 3** — Application logic and database operations
- **SQLite** — Relational database management
- **Tkinter** — Graphical user interface for property listings
- **Pillow** — Image processing and display
- **dbdiagram.io** — Relational schema visualization

## 🗃️ Database Structure

The database consists of six interconnected tables:

| Table | Description | Records |
|---|---|---:|
| Agent | Real estate agent information | 9 |
| Buyer | Property buyer information | 20 |
| Seller | Property owner information | 20 |
| Property | Property details, locations, and images | 40 |
| Listing | Listing prices, dates, statuses, and associated agents | 40 |
| Sale | Completed property transactions | 16 |
| **Total** | | **145** |

Primary and foreign keys establish relationships between tables and maintain referential integrity.

## ✨ Key Features

### Property Management
- Store and retrieve residential and commercial property information.
- Manage property listings, prices, and availability.
- Display property images and details through a graphical interface.

### SQL Queries and Analysis
The project implements ten database queries and operations, including:

1. Search available properties within a specified location and price range.
2. Find properties matching bedroom and pool requirements.
3. Identify the highest-performing real estate agent by sales volume.
4. Calculate average sale prices and listing-to-closing times by agent.
5. Retrieve the most expensive property and display its image.
6. Record and verify completed property sales.
7. Add and verify new real estate agents.
8. Identify properties priced above their neighborhood average.
9. Calculate buyer savings by comparing listing and sale prices.
10. Search for available homes using customizable buyer preferences.

### Database Transactions
Property sales are recorded using SQL transactions to ensure that sale records and listing statuses are updated together.

### Data Validation
Six validation checks verify:
- Table record counts
- Foreign key integrity
- Database integrity
- Listing and sale consistency
- Sale date validity
- Duplicate property detection

All six checks passed during project testing.

---

## 💻 Installation and Setup

### Prerequisites

Before running the project, ensure you have:

- **Python 3** installed
- **pip** available for installing Python packages
- **SQLite support**, provided by Python's built-in `sqlite3` module

SQLite generally does not require a separate installation when using Python.

To verify SQLite support, run:

```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

If a version number appears, SQLite is available.

**Optional:** Install [DB Browser for SQLite](https://sqlitebrowser.org/) to visually inspect database tables and records.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

Replace the placeholders with the actual GitHub repository URL and folder name.

### 2. Install Dependencies

The project uses Python's built-in `sqlite3`, `tkinter`, and `pathlib` modules, along with Pillow for image display.

Install Pillow:

```bash
python -m pip install pillow
```

Tkinter is included with many standard Python installations. If it is unavailable, it may require a separate installation depending on your operating system and Python distribution.

### 3. Access the Database

The repository includes a populated SQLite database:

`real_estate.db`

**Recommended:** Use the existing database to explore the completed project, including all sample listings, sales, and agent records.

There is no need to recreate the database before running queries.

To initialize a new database from scratch, use the database creation and population scripts:

```bash
python create_db.py
python populate.py
```

**Important:** Database initialization should only be performed when setting up a new database. Reinitializing or modifying the existing database may alter stored records or transaction history.

### 4. Run SQL Queries

Execute the database queries:

```bash
python queries.py
```

This displays property searches, sales performance, market comparisons, and transaction information in the console.

### 5. Launch the Property Gallery

```bash
python property_gallery.py
```

The gallery displays eight featured properties with images, addresses, listing prices, bedrooms, bathrooms, and availability statuses.

Ensure that the `images/` directory is included in the project, as property image paths are stored in the database.

### 6. Validate the Database

```bash
python validate_database.py
```

This executes six validation checks to verify database integrity and consistency.

### 7. Additional Database Operations

The project also includes scripts for demonstrating database modifications:

- `record_sale.py` — Records a completed property sale and updates the associated listing.
- `add_agent.py` — Inserts a new real estate agent.
- `add_images.py` — Updates property image paths.

**Note:** These scripts modify database records. Use a backup or fresh database when repeating transaction demonstrations.

---

## 📊 Example Query Results

| Feature | Result |
|---|---|
| Most Expensive Property | King Neptune's Palace — $8,500,000 |
| Properties Above City Average | 16 |
| Largest Buyer Savings | Mrs. Puff — $70,000 |
| Example Completed Sale | Gary Snail purchased 124 Conch Street for $415,000 |
| Database Integrity | 6/6 validation checks passed |
| Property Gallery | 8 featured properties |

These results were obtained using the project's fictional sample dataset.

## 📁 Project Organization

```text
real-estate-database/
├── images/
│   └── ...                  # Property image files
├── real_estate.db           # Populated SQLite database
├── create_db.py             # Database schema creation
├── populate.py              # Sample data population
├── queries.py               # SQL queries and analysis
├── record_sale.py           # Property sale transaction
├── add_agent.py             # Agent insertion
├── add_images.py            # Property image updates
├── property_gallery.py      # Tkinter property gallery
├── validate_database.py     # Database integrity checks
└── README.md                # Project documentation
```

## 🎓 Academic Purpose

This project demonstrates practical database management concepts, including:

- Relational database design and normalization
- Primary keys and foreign key relationships
- SQL joins, subqueries, and aggregate functions
- Parameterized queries and filtering
- Database transactions and data consistency
- Data validation and integrity checking
- Python database connectivity
- Basic graphical interface development

## 👩🏽‍💻 Project Team

**Raina Bethea**  
**Kyla Franklin**

Georgia State University  
Database Systems — Fall 2026

## 📌 Disclaimer

Bikini Bottom Realty is an educational project. All property listings, prices, and transactions are fictional.

*SpongeBob SquarePants* and associated characters, locations, and artwork are the intellectual property of their respective owners. Referenced imagery is used solely for educational demonstration purposes.