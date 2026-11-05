
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "real_estate.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

print("BIKINI BOTTOM REALTY - DATABASE VALIDATION")
print("=" * 55)

# check 1: table record counts
print("\nCHECK 1: TABLE RECORD COUNTS")

tables = ["Agent", "Buyer", "Seller", "Property", "Listing", "Sale"]

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table};")
    count = cursor.fetchone()[0]
    print(f"{table}: {count} records")

# check 2: foreign key integrity
print("\nCHECK 2: FOREIGN KEY INTEGRITY")

cursor.execute("PRAGMA foreign_key_check;")
violations = cursor.fetchall()

if not violations:
    print("PASS: No foreign key violations found.")
else:
    print(f"FAIL: {len(violations)} foreign key violations found.")
    for violation in violations:
        print(violation)

# check 3: general database integrity
print("\nCHECK 3: DATABASE INTEGRITY")

cursor.execute("PRAGMA integrity_check;")
integrity = cursor.fetchall()

if integrity == [("ok",)]:
    print("PASS: Database integrity verified.")
else:
    print("FAIL: Database integrity issues detected.")
    for issue in integrity:
        print(issue)


# check 4: Listing and Sale consistency
print("\nCHECK 4: LISTING AND SALE CONSISTENCY")

cursor.execute("""
SELECT l.listing_id, l.status
FROM Listing l
LEFT JOIN Sale s ON l.listing_id = s.listing_id
WHERE (l.status = 'Sold' AND s.sale_id IS NULL)
   OR (l.status = 'Available' AND s.sale_id IS NOT NULL);
""")

inconsistencies = cursor.fetchall()

if not inconsistencies:
    print("PASS: All listing statuses match their sale records.")
else:
    print(f"FAIL: {len(inconsistencies)} inconsistent listings.")
    for record in inconsistencies:
        print(record)


# check 5: Sale dates must follow listing dates
print("\nCHECK 5: SALE DATE VALIDATION")

cursor.execute("""
SELECT s.sale_id, l.listing_date, s.sale_date
FROM Sale s
JOIN Listing l ON s.listing_id = l.listing_id
WHERE date(s.sale_date) < date(l.listing_date)
   OR date(s.sale_date) IS NULL
   OR date(l.listing_date) IS NULL;
""")

invalid_dates = cursor.fetchall()

if not invalid_dates:
    print("PASS: All sales occurred on or after listing dates.")
else:
    print(f"FAIL: {len(invalid_dates)} invalid sale dates.")
    for record in invalid_dates:
        print(record)


# check 6: Duplicate property addresses
print("\nCHECK 6: DUPLICATE PROPERTIES")

cursor.execute("""
SELECT address, city, COUNT(*) AS duplicates
FROM Property
GROUP BY LOWER(TRIM(address)), LOWER(TRIM(city)), state
HAVING COUNT(*) > 1;
""")

duplicates = cursor.fetchall()

if not duplicates:
    print("PASS: No duplicate property addresses found.")
else:
    print(f"FAIL: {len(duplicates)} duplicate property groups.")
    for record in duplicates:
        print(record)

conn.close()
