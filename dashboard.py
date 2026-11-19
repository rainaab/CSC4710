import tkinter as tk
from tkinter import ttk

import sqlite3
from pathlib import Path
from tkinter import messagebox
from datetime import date
from PIL import Image, ImageTk

# Bikini Bottom color palette
OCEAN_BLUE = "#087EAD"
DEEP_BLUE = "#064663"
PINEAPPLE_YELLOW = "#FFE45C"
SAND = "#FFF7D6"
WHITE = "#FFFFFF"

DB_PATH = Path(__file__).resolve().parent / "real_estate.db"

def main():
    root = tk.Tk()
    root.title("Bikini Bottom Realty")
    root.geometry("1150x850")
    root.minsize(850, 600)
    root.configure(bg=OCEAN_BLUE)

    # Configure the standard Tkinter widgets.
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        "TNotebook",
        background=OCEAN_BLUE,
        borderwidth=0,
    )
    style.configure(
        "TNotebook.Tab",
        background=SAND,
        foreground=DEEP_BLUE,
        font=("Arial", 12, "bold"),
        padding=(20, 12),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", PINEAPPLE_YELLOW)],
        foreground=[("selected", DEEP_BLUE)],
    )

    style.configure("Treeview", font=("Arial", 11), rowheight=32,
                    background=WHITE, fieldbackground=WHITE, foreground=DEEP_BLUE)
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"),
                    background=PINEAPPLE_YELLOW, foreground=DEEP_BLUE)
    style.map("Treeview", background=[("selected", OCEAN_BLUE)],
              foreground=[("selected", WHITE)])

    # Header
    header = tk.Frame(root, bg=OCEAN_BLUE)
    header.pack(fill="x", padx=30, pady=(25, 20))

    tk.Label(
        header,
        text="BIKINI BOTTOM REALTY",
        font=("Arial", 28, "bold"),
        bg=OCEAN_BLUE,
        fg=PINEAPPLE_YELLOW,
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Find your dream home under the sea!",
        font=("Arial", 13),
        bg=OCEAN_BLUE,
        fg=WHITE,
    ).pack(anchor="w", pady=(5, 0))

    # Navigation tabs
    notebook = ttk.Notebook(root)
    notebook.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=(0, 25),
    )

    search_tab = tk.Frame(notebook, bg=SAND)
    market_tab = tk.Frame(notebook, bg=SAND)
    longest_tab = tk.Frame(notebook, bg=SAND)

    notebook.add(search_tab, text="Find a Home")
    notebook.add(market_tab, text="City Market")
    notebook.add(longest_tab, text="Longest Listed")

    # Home search controls
    tk.Label(
        search_tab,
        text="Find your own piece of Bikini Bottom",
        font=("Arial", 20, "bold"),
        bg=SAND,
        fg=DEEP_BLUE,
    ).pack(anchor="w", padx=25, pady=(25, 15))

    filters = tk.Frame(search_tab, bg=SAND)
    filters.pack(fill="x", padx=25)

    city_var = tk.StringVar(value="Any")
    budget_var = tk.StringVar(value="600000")
    bedrooms_var = tk.StringVar(value="2")
    bathrooms_var = tk.StringVar(value="0")
    pool_var = tk.BooleanVar(value=False)

    # Each field gets a label above its input.
    for column, label in enumerate(
        ["City", "Maximum budget ($)", "Minimum bedrooms", "Minimum bathrooms"]
    ):
        tk.Label(
            filters,
            text=label,
            font=("Arial", 11, "bold"),
            bg=SAND,
            fg=DEEP_BLUE,
        ).grid(row=0, column=column, sticky="w", padx=(0, 20))

    city_input = ttk.Combobox(
        filters,
        textvariable=city_var,
        values=["Any", "Bikini Bottom", "Jellyfish Fields"],
        state="readonly",
        width=22,
    )

    # Load the city choices from the database.
    try:
        conn = sqlite3.connect(
            DB_PATH.as_uri() + "?mode=ro",
            uri=True,
        )
        try:
            cities = conn.execute("""
                SELECT DISTINCT city
                FROM Property
                WHERE city IS NOT NULL
                ORDER BY city;
            """).fetchall()
        finally:
            conn.close()

        city_input["values"] = ["Any"] + [
            city for (city,) in cities
        ]
    except sqlite3.Error as error:
        messagebox.showerror("Could not load cities", str(error))

    city_input.grid(
        row=1, column=0, sticky="w", padx=(0, 20), pady=8
    )

    budget_input = ttk.Entry(
        filters,
        textvariable=budget_var,
        width=18,
    )
    budget_input.grid(
        row=1, column=1, sticky="w", padx=(0, 20), pady=8
    )

    bedrooms_input = ttk.Spinbox(
        filters,
        textvariable=bedrooms_var,
        from_=0,
        to=20,
        width=10,
    )
    bedrooms_input.grid(
        row=1, column=2, sticky="w", pady=8
    )

    bathrooms_input = ttk.Spinbox(
        filters,
        textvariable=bathrooms_var,
        from_=0,
        to=20,
        increment=0.5,
        width=10,
    )
    bathrooms_input.grid(row=1, column=3, sticky="w", pady=8)

    tk.Checkbutton(
        filters,
        text="Must have a pool",
        variable=pool_var,
        bg=SAND,
        fg=DEEP_BLUE,
        activebackground=SAND,
        font=("Arial", 11),
    ).grid(row=2, column=0, sticky="w", pady=10)

    status_var = tk.StringVar(
        value="Choose your preferences, then search."
    )

    
    def search_homes():
        # Check input before sending it to the database.
        try:
            budget = float(budget_var.get().replace(",", "").strip())
            bedrooms = int(bedrooms_var.get())
            bathrooms = float(bathrooms_var.get())

            if not 0 <= budget <= 1_000_000_000 or bedrooms < 0:
                raise ValueError
            if not 0 <= bathrooms <= 20 or bathrooms % 0.5 != 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Check your search",
                "Enter a budget between 0 and 1 billion "
                "and a nonnegative whole number of bedrooms. "
                "Bathrooms must be between 0 and 20 in half-bath steps (such as 1.5).",
            )
            return

        city = city_var.get()

        sql = """
            SELECT
                p.address,
                p.city,
                p.bedrooms,
                p.bathrooms,
                l.list_price,
                p.image_url
            FROM Property p
            JOIN Listing l ON p.property_id = l.property_id
            WHERE l.status = 'Available'
                AND p.property_type != 'Commercial'
                AND l.list_price <= ?
                AND p.bedrooms >= ?
                AND p.bathrooms >= ?
                AND (? = 'Any' OR p.city = ?)
                AND (? = 0 OR p.has_pool = 1)
            ORDER BY l.list_price ASC;
        """

        try:
            # Read-only mode protects the existing project data.
            conn = sqlite3.connect(
                DB_PATH.as_uri() + "?mode=ro",
                uri=True,
            )
            try:
                homes = conn.execute(
                    sql,
                    (budget, bedrooms, bathrooms, city, city, int(pool_var.get())),
                ).fetchall()
            finally:
                conn.close()
        except sqlite3.Error as error:
            messagebox.showerror("Database error", str(error))
            return

        # Clear the previous search results.
        for item in results_table.get_children():
            results_table.delete(item)

        home_images.clear()
        clear_preview()
        for address, home_city, beds, baths, price, image_path in homes:
            item_id = results_table.insert(
                "",
                "end",
                values=(
                    address,
                    home_city,
                    beds,
                    baths,
                    f"${price:,.2f}",
                ),
            )

            home_images[item_id] = (address, image_path)

        status_var.set(
            f"Found {len(homes)} matching homes."
            if homes
            else "No homes match. Try increasing your budget "
                 "or relaxing a filter."
        )

    tk.Button(
        filters,
        text="SEARCH HOMES",
        command=search_homes,
        bg=PINEAPPLE_YELLOW,
        fg=DEEP_BLUE,
        activebackground=WHITE,
        font=("Arial", 11, "bold"),
        relief="flat",
        padx=20,
        pady=10,
        cursor="hand2",
    ).grid(row=2, column=1, columnspan=3, sticky="e", pady=10)

    tk.Label(
        search_tab,
        textvariable=status_var,
        bg=SAND,
        fg=DEEP_BLUE,
        font=("Arial", 11),
        wraplength=750,
        justify="left",
    ).pack(anchor="w", padx=25, pady=20)
    for tab, heading in [
        (market_tab, "Explore the Bikini Bottom market"),
        (longest_tab, "Homes still waiting for a buyer"),
    ]:
        tk.Label(
            tab,
            text=heading,
            font=("Arial", 20, "bold"),
            bg=SAND,
            fg=DEEP_BLUE,
        ).pack(anchor="w", padx=25, pady=25)

    # Table displaying the matching properties
    table_frame = tk.Frame(search_tab, bg=SAND)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 20),
    )

    columns = ("address", "city", "beds", "baths", "price")

    results_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=6,
    )

    for column, heading, width in [
        ("address", "Address", 250),
        ("city", "City", 170),
        ("beds", "Beds", 65),
        ("baths", "Baths", 65),
        ("price", "Asking Price", 130),
    ]:
        results_table.heading(column, text=heading)
        results_table.column(column, width=width, anchor="w")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=results_table.yview,
    )
    results_table.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    results_table.pack(side="left", fill="both", expand=True)

    # Keep the PhotoImage alive while its preview is displayed.
    home_images = {}
    preview = tk.Frame(search_tab, bg=WHITE, height=300)
    preview.pack(
        side="bottom",
        fill="x",
        padx=25,
        pady=(0, 20)
    )
    preview.pack_propagate(False)
    preview_image = tk.Label(preview, bg=WHITE, fg=DEEP_BLUE)
    preview_image.pack(side="left", padx=15, pady=10)
    preview_text = tk.Label(preview, text="Select a home to see its photo.",
                            bg=WHITE, fg=DEEP_BLUE, font=("Arial", 12, "bold"))
    preview_text.pack(side="left", padx=15)

    def clear_preview():
        preview_image.configure(image="", text="")
        preview_image.image = None
        preview_text.configure(text="Select a home to see its photo.")

    def show_preview(event=None):
        selection = results_table.selection()
        if not selection or selection[0] not in home_images:
            return
        address, image_path = home_images[selection[0]]
        clear_preview()
        preview_text.configure(text=address)
        if image_path:
            try:
                with Image.open(DB_PATH.parent / image_path) as source:
                    picture = source.copy()
                picture.thumbnail((400, 250), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(picture)
                preview_image.configure(
                    image=photo,
                    text="",
                    width=400,
                    height=250
                )
                preview_image.image = photo
                preview_image.update_idletasks()
                return
            except (OSError, ValueError):
                pass
        preview_image.configure(text="No photo available", width=24, height=6)

    results_table.bind("<<TreeviewSelect>>", show_preview)
    budget_input.bind("<Return>", lambda event: search_homes())
    bedrooms_input.bind("<Return>", lambda event: search_homes())
    bathrooms_input.bind("<Return>", lambda event: search_homes())

    # City market summary
    market_columns = ("city", "available", "average", "lowest", "highest")

    market_table = ttk.Treeview(
        market_tab,
        columns=market_columns,
        show="headings",
        height=12,
    )

    for column, heading, width in [
        ("city", "City", 200),
        ("available", "Available Listings", 140),
        ("average", "Average Price", 150),
        ("lowest", "Lowest Price", 150),
        ("highest", "Highest Price", 150),
    ]:
        market_table.heading(column, text=heading)
        market_table.column(column, width=width, anchor="w")

    market_table.pack(fill="both", expand=True, padx=25, pady=15)

    def load_city_market():
        sql = """
            SELECT
                p.city,
                COUNT(*) AS available_homes,
                AVG(l.list_price) AS average_price,
                MIN(l.list_price) AS lowest_price,
                MAX(l.list_price) AS highest_price
            FROM Property p
            JOIN Listing l ON p.property_id = l.property_id
            WHERE l.status = 'Available'
                AND p.property_type != 'Commercial'
            GROUP BY p.city
            ORDER BY average_price DESC;
        """

        try:
            conn = sqlite3.connect(
                DB_PATH.as_uri() + "?mode=ro",
                uri=True,
            )
            try:
                rows = conn.execute(sql).fetchall()
            finally:
                conn.close()
        except sqlite3.Error as error:
            messagebox.showerror("Database error", str(error))
            return

        for item in market_table.get_children():
            market_table.delete(item)

        for city, count, average, lowest, highest in rows:
            market_table.insert(
                "",
                "end",
                values=(
                    city,
                    count,
                    f"${average:,.2f}",
                    f"${lowest:,.2f}",
                    f"${highest:,.2f}",
                ),
            )

    # Longest-listed query: the chosen date makes the demo reproducible.
    date_controls = tk.Frame(longest_tab, bg=SAND)
    date_controls.pack(fill="x", padx=25, pady=(0, 15))
    tk.Label(date_controls, text="As of (YYYY-MM-DD):", bg=SAND,
             fg=DEEP_BLUE, font=("Arial", 11)).pack(side="left")
    as_of_var = tk.StringVar(value=date.today().isoformat())
    ttk.Entry(date_controls, textvariable=as_of_var, width=14).pack(side="left", padx=10)
    longest_status = tk.StringVar()
    tk.Label(longest_tab, textvariable=longest_status, bg=SAND,
             fg=DEEP_BLUE).pack(anchor="w", padx=25)

    longest_frame = tk.Frame(longest_tab, bg=SAND)
    longest_frame.pack(fill="both", expand=True, padx=25, pady=15)
    longest_table = ttk.Treeview(longest_frame,
        columns=("address", "city", "price", "listed", "days"), show="headings")
    for column, heading, width in [
        ("address", "Address", 240), ("city", "City", 180),
        ("price", "Asking Price", 130), ("listed", "Listed On", 120),
        ("days", "Days Listed", 100),
    ]:
        longest_table.heading(column, text=heading)
        longest_table.column(column, width=width, anchor="w")
    longest_scroll = ttk.Scrollbar(longest_frame, orient="vertical",
                                   command=longest_table.yview)
    longest_table.configure(yscrollcommand=longest_scroll.set)
    longest_scroll.pack(side="right", fill="y")
    longest_table.pack(fill="both", expand=True)

    def load_longest_listed():
        try:
            as_of = date.fromisoformat(as_of_var.get().strip()).isoformat()
        except ValueError:
            messagebox.showerror("Check the date", "Use a valid date in YYYY-MM-DD format.")
            return
        sql = """
            SELECT p.address, p.city, l.list_price, l.listing_date,
                   CAST(julianday(?) - julianday(l.listing_date) AS INTEGER) AS days_listed
            FROM Property p
            JOIN Listing l ON p.property_id = l.property_id
            WHERE l.status = 'Available'
              AND p.property_type != 'Commercial'
              AND date(l.listing_date) <= date(?)
            ORDER BY days_listed DESC, l.listing_id;
        """
        try:
            conn = sqlite3.connect(DB_PATH.as_uri() + "?mode=ro", uri=True)
            try:
                rows = conn.execute(sql, (as_of, as_of)).fetchall()
            finally:
                conn.close()
        except sqlite3.Error as error:
            messagebox.showerror("Database error", str(error))
            return
        for item in longest_table.get_children():
            longest_table.delete(item)
        for address, city, price, listed, days in rows:
            longest_table.insert("", "end", values=(address, city, f"${price:,.2f}", listed, days))
        longest_status.set(
            f"{len(rows)} currently available residential listings, aged through {as_of}."
            if rows else "No available listings on or before this date."
        )

    tk.Button(date_controls, text="UPDATE", command=load_longest_listed,
              bg=PINEAPPLE_YELLOW, fg=DEEP_BLUE, relief="flat",
              font=("Arial", 11, "bold"), padx=15).pack(side="left")
    tk.Label(longest_tab,
             text="Uses current availability; changing the date does not recreate historical inventory.",
             bg=SAND, fg=DEEP_BLUE).pack(anchor="w", padx=25, pady=(0, 20))

    load_city_market()
    load_longest_listed()
    search_homes()

    root.mainloop()


if __name__ == "__main__":
    main()
