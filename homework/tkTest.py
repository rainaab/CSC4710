import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("FIFA TEST 2026")
root.geometry("900x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

teamsTab = ttk.Frame(notebook)
notebook.add(teamsTab, text="Teams")
playersTab = ttk.Frame(notebook)
notebook.add(playersTab, text="Players")
matchesTab = ttk.Frame(notebook)
notebook.add(matchesTab, text="Matches")
searchTab = ttk.Frame(notebook)
notebook.add(searchTab, text="Search")


root.mainloop()