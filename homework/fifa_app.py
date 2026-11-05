import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

################################################################################
# Database Setup

# database connection
conn = sqlite3.connect('fifa.db')
c = conn.cursor()

# table for each team
c.execute("""
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,  
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    coach TEXT
)
""")

# table for each player
c.execute("""
CREATE TABLE IF NOT EXISTS players (
    team_id INTEGER NOT NULL,
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    jersey_number INTEGER NOT NULL,
    position TEXT NOT NULL,
    
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
)
""")

# table for each match
c.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_date TEXT NOT NULL,
    stadium TEXT NOT NULL,
    team_id1 INTEGER NOT NULL,
    team_id2 INTEGER NOT NULL,
    score_t1 INTEGER,
    score_t2 INTEGER,
    
    FOREIGN KEY (team_id1) REFERENCES teams(team_id),
    FOREIGN KEY (team_id2) REFERENCES teams(team_id)
)
""")

# insert some data for teams
#c.execute("""
#INSERT INTO teams (name, country, coach) VALUES ("The Reds","Canada","Jesse Marsch")
#    """)
#c.execute("""
#INSERT INTO teams (name, country, coach) VALUES ("El Tri","Mexico","Javier Aguirre")
#    """)
#c.execute("""
#INSERT INTO teams (name, country, coach) VALUES ("The Stars and Stripes","USA","Mauricio Pochettino")
#    """)
# teams = [
#     ("Zmajevi AKA The Dragons ", "Bosnia and Herzegovina", "Sergej Barbarez"), #4
#     ("Bafana Bafana", "South Africa","Hugo Broos"), #5
#     ("La Albirroja", "Paraguay", "Gustavo Alfaro"), #6
# ]
# c.executemany("""
# INSERT INTO teams (name, country, coach)
#     VALUES (?, ?, ?)
#    """, teams)

# insert some player data
# players = [
#     (1, "Dayne St.Clair", 1 , "Goalkeeper"), # Canada
#     (1, "Jayden Nelson", 26 , "Forward"), #Canada
#     (2, "Raul Jimenez", 9, "Forward"), #Mexico
#     (2, "Orbelin Pineda", 17, "Midfielder"), #Mexico
#     (3, "Matt Freese", 24, "Goalkeeper"), #USA
#     (3, "Chris Richards", 26, "Defender"), #USA
# ]
# c.executemany("""
# INSERT INTO players (team_id, name, jersey_number, position)
#     VALUES (?, ?, ?, ?)
# """, players)

# # insert some match data
# # matches = [
# #     ("June 11, 2026", "Mexico City Stadium", 2, 5, 2, 0),
# #     ("June 12, 2026", "Toronto Stadium", 1, 4, 1, 1 ),
# #     ("June 12, 2026", "Los Angeles Stadium", 3, 6, 4, 1)
# # ]
# c.executemany("""
# INSERT INTO matches (match_date, stadium, team_id1, team_id2, score_t1, score_t2)
#     VALUES (?, ?, ?, ?, ?, ?)
#    """, matches)
# conn.commit()

# c.execute("""
# SELECT * FROM teams
# """)
# teams = c.fetchall()
# for team in teams:
#     print(team)
#
# c.execute("""
# SELECT * FROM players
# """)
# players = c.fetchall()
# for player in players:
#     print(player)
#
# c.execute("""
# SELECT * FROM matches
# """)
# matches = c.fetchall()
# for match in matches:
#     print(match)

##############################################################################
# GUI Setup
root = tk.Tk()
root.title("FIFA 2026")
root.geometry("900x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# creating tabs
teamsTab = ttk.Frame(notebook)
notebook.add(teamsTab, text="Teams")
playersTab = ttk.Frame(notebook)
notebook.add(playersTab, text="Players")
matchesTab = ttk.Frame(notebook)
notebook.add(matchesTab, text="Matches")
searchTab = ttk.Frame(notebook)
notebook.add(searchTab, text="Search")

################################################################################
# teams tab
teamsForm = ttk.Frame(teamsTab)
teamsForm.pack(pady=20)

ttk.Label(teamsForm, text="Team Name:").grid(column=0, row=0, padx=5, pady=5)
teamNameEntry = ttk.Entry(teamsForm, width=25)
teamNameEntry.grid(column=1, row=0, padx=5, pady=5)

ttk.Label(teamsForm, text="Country:").grid(column=0, row=1, padx=5, pady=5)
countryEntry = ttk.Entry(teamsForm, width=25)
countryEntry.grid(column=1, row=1, padx=5, pady=5)

ttk.Label(teamsForm, text="Coach Name:").grid(column=0, row=2, padx=5, pady=5)
coachNameEntry = ttk.Entry(teamsForm, width=25)
coachNameEntry.grid(column=1, row=2, padx=5, pady=5)

# display table
teamTable = ttk.Treeview(teamsTab,
                         columns=("team_id", "name", "country", "coach"),
                         show="headings")
teamTable.heading('team_id', text='ID')
teamTable.heading('name', text='Team Name')
teamTable.heading('country', text='Country')
teamTable.heading('coach', text='Coach Name')

teamTable.column('team_id', anchor='center')
teamTable.column('name', anchor='center')
teamTable.column('country', anchor='center')
teamTable.column('coach', anchor='center')

teamTable.pack(fill="both", expand=True, padx=5, pady=5)

def loadTeams():
    for row in teamTable.get_children():
        teamTable.delete(row)

    c.execute('SELECT * FROM teams')
    teams = c.fetchall()

    for team in teams:
        teamTable.insert('', 'end', values=team)
# function to add teams
def addTeams():
    name = teamNameEntry.get()
    country = countryEntry.get()
    coach = coachNameEntry.get()

    c.execute("""
    INSERT INTO teams(name, country, coach)     
    VALUES (?, ?, ?)""", (name, country, coach))

    conn.commit()

    teamNameEntry.delete(0, 'end')
    countryEntry.delete(0, 'end')
    coachNameEntry.delete(0, 'end')
    loadTeams()
    teamTable.update()

# select/ update functionality
def selectTeam(event):
    selected = teamTable.selection()
    if selected:
        team = teamTable.item(selected[0])["values"]
        teamNameEntry.delete(0, "end")
        countryEntry.delete(0, "end")
        coachNameEntry.delete(0, "end")

        teamNameEntry.insert(0, team[1])
        countryEntry.insert(0, team[2])
        coachNameEntry.insert(0, team[3])
# update team
def updateTeam():
    selected = teamTable.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a team to update.")
        return
    team = teamTable.item(selected[0])["values"]
    team_id = team[0]
    name = teamNameEntry.get()
    country = countryEntry.get()
    coach = coachNameEntry.get()

    c.execute("""
        UPDATE teams
        SET name = ?, country = ?, coach = ?
        WHERE team_id = ?
    """, (name, country, coach, team_id))

    conn.commit()

    teamNameEntry.delete(0, "end")
    countryEntry.delete(0, "end")
    coachNameEntry.delete(0, "end")

    loadTeams()
    teamTable.update()
## delete team function
def deleteTeam():
    selected = teamTable.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a team to delete.")
        return

    team = teamTable.item(selected[0])["values"]
    team_id = team[0]

    c.execute("""
        DELETE FROM teams
        WHERE team_id = ?
    """, (team_id,))

    conn.commit()

    teamNameEntry.delete(0, "end")
    countryEntry.delete(0, "end")
    coachNameEntry.delete(0, "end")

    loadTeams()

    teamTable.update()
## buttons
addTeamButton = ttk.Button(teamsForm, text="Add Teams", command=addTeams)
addTeamButton.grid(column=0, row=3, padx=5, pady=10)
teamTable.bind("<<TreeviewSelect>>", selectTeam)

updateTeamButton = ttk.Button(teamsForm,text="Update Team",command=updateTeam)
updateTeamButton.grid(column=1, row=3, padx=5, pady=10)

deleteTeamButton = ttk.Button(teamsForm,text="Delete Team",command=deleteTeam)
deleteTeamButton.grid(column=2, row=3, padx=5, pady=10)

loadTeams()

# players tab
playersForm = ttk.Frame(playersTab)
playersForm.pack(pady=20)
## get team names for id dropdown
c.execute("SELECT team_id, name FROM teams")
teamList = c.fetchall()
# maps team name to team ID
teamMap = {name: team_id for team_id, name in teamList}

ttk.Label(playersForm, text="Team:").grid(column=0, row=0, padx=5, pady=5)
playersTeam = ttk.Combobox(playersForm, values=list(teamMap.keys()), state="readonly",width=25)
playersTeam.grid(column=1, row=0, padx=5, pady=5)

ttk.Label(playersForm, text="Player Name:").grid(column=0, row=1, padx=5, pady=5)
playersNameEntry = ttk.Entry(playersForm, width=25)
playersNameEntry.grid(column=1, row=1, padx=5, pady=5)

ttk.Label(playersForm, text="Jersey Number:").grid(column=0, row=2, padx=5, pady=5)
jerseyEntry = ttk.Entry(playersForm, width=25)
jerseyEntry.grid(column=1, row=2, padx=5, pady=5)

ttk.Label(playersForm, text="Position:").grid(column=0, row=3, padx=5, pady=5)
positionEntry = ttk.Entry(playersForm, width=25)
positionEntry.grid(column=1, row=3, padx=5, pady=5)

# display table
playersTable = ttk.Treeview(playersTab,
                         columns=("player_id", "name", "team", "jersey_number", "position"),
                         show="headings")
playersTable.heading('player_id', text='ID')
playersTable.heading('name', text='Player Name')
playersTable.heading('team', text='Team')
playersTable.heading('jersey_number', text='Jersey Number')
playersTable.heading('position', text='Position')

playersTable.column('player_id', anchor='center')
playersTable.column('name', anchor='center')
playersTable.column('team', anchor='center')
playersTable.column('jersey_number', anchor='center')
playersTable.column('position', anchor='center')

playersTable.pack(fill="both", expand=True, padx=5, pady=5)

def loadPlayers():
    for row in playersTable.get_children():
        playersTable.delete(row)

    c.execute('''SELECT players.player_id, 
                        players.name, 
                        teams.name, 
                        players.jersey_number,
                        players.position 
                 FROM players
              JOIN teams ON players.team_id = teams.team_id''')

    players = c.fetchall()

    for player in players:
        playersTable.insert('', 'end', values=player)
# function to add teams
def addPlayers():
    selectedTeam = playersTeam.get()
    if not selectedTeam:
        messagebox.showerror("Missing Team", "Please select a team")
        return
    team = teamMap[selectedTeam]

    name = playersNameEntry.get()
    jersey_number = jerseyEntry.get()
    position = positionEntry.get()

    c.execute("""
    INSERT INTO players(team_id, name, jersey_number, position)     
    VALUES (?, ?, ?, ?)""", (team, name, jersey_number, position))

    conn.commit()

    playersTeam.set("")
    playersNameEntry.delete(0, 'end')
    jerseyEntry.delete(0, 'end')
    positionEntry.delete(0, 'end')

    loadPlayers()
    playersTable.update()

# select/ update functionality
def selectPlayer(event):
    selected = playersTable.selection()
    if selected:
        player = playersTable.item(selected[0])["values"]
        playersTeam.set(player[2])
        playersNameEntry.delete(0, "end")
        jerseyEntry.delete(0, "end")
        positionEntry.delete(0, "end")

        playersNameEntry.insert(0, player[1])
        jerseyEntry.insert(0, player[2])
        positionEntry.insert(0, player[3])
playersTable.bind("<<TreeviewSelect>>", selectPlayer)

# update player
def updatePlayer():
    selected = playersTable.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a player to update.")
        return
    player = playersTable.item(selected[0])["values"]
    player_id = player[0]
    selectedTeam = playersTeam.get()
    team = teamMap[selectedTeam]
    name = playersNameEntry.get()
    jersey_number = jerseyEntry.get()
    position = positionEntry.get()

    c.execute("""
        UPDATE players
        SET team_id = ?, name = ?, jersey_number = ?, position = ?
        WHERE player_id = ?
    """, (team, name, jersey_number, position, player_id))

    conn.commit()

    playersTeam.set("")
    playersNameEntry.delete(0, "end")
    jerseyEntry.delete(0, "end")
    positionEntry.delete(0, "end")

    loadPlayers()
    playersTable.update()
## delete player function
def deletePlayer():
    selected = playersTable.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a player to delete.")
        return

    player = playersTable.item(selected[0])["values"]
    player_id = player[0]

    c.execute("""
        DELETE FROM players
        WHERE player_id = ?
    """, (player_id,))

    conn.commit()

    playersTeam.set("")
    playersNameEntry.delete(0, "end")
    jerseyEntry.delete(0, "end")
    positionEntry.delete(0, "end")

    loadPlayers()

    playersTable.update()
## buttons
addPlayerButton = ttk.Button(playersForm, text="Add Players", command=addPlayers)
addPlayerButton.grid(column=0, row=4, padx=5, pady=10)
playersTable.bind("<<TreeviewSelect>>", selectPlayer)

updatePlayerButton = ttk.Button(playersForm,text="Update Player",command=updatePlayer)
updatePlayerButton.grid(column=1, row=4, padx=5, pady=10)

deletePlayerButton = ttk.Button(playersForm,text="Delete Player",command=deletePlayer)
deletePlayerButton.grid(column=2, row=4, padx=5, pady=10)

################################################################################
# matches tab
matchesForm = ttk.Frame(matchesTab)
matchesForm.pack(pady=20)

ttk.Label(matchesForm,text="Date:").grid(column=0, row=0, padx=5, pady=5)
matchDateEntry = ttk.Entry(matchesForm, width=25)
matchDateEntry.grid(column=1, row=0, padx=5, pady=5)

ttk.Label(matchesForm,text="Stadium:").grid(column=0, row=1, padx=5, pady=5)
stadiumEntry = ttk.Entry(matchesForm, width=25)
stadiumEntry.grid(column=1, row=1, padx=5, pady=5)

ttk.Label(matchesForm,text="Team 1:").grid(column=0, row=2, padx=5, pady=5)
team1 = ttk.Combobox(matchesForm,values=list(teamMap.keys()),state="readonly",width=23)
team1.grid(column=1, row=2, padx=5, pady=5)

ttk.Label(matchesForm,text="Team 2:").grid(column=0, row=3, padx=5, pady=5)
team2 = ttk.Combobox(matchesForm,values=list(teamMap.keys()),state="readonly",width=23)
team2.grid(column=1, row=3, padx=5, pady=5)

ttk.Label(matchesForm,text="Team 1 Score:").grid(column=0, row=4, padx=5, pady=5)
score1Entry = ttk.Entry(matchesForm, width=25)
score1Entry.grid(column=1, row=4, padx=5, pady=5)

ttk.Label(matchesForm,text="Team 2 Score:").grid(column=0, row=5, padx=5, pady=5)
score2Entry = ttk.Entry(matchesForm, width=25)
score2Entry.grid(column=1, row=5, padx=5, pady=5)

## display table
matchesTable = ttk.Treeview(
    matchesTab,
    columns=(
        "match_id",
        "date",
        "stadium",
        "team1",
        "team2",
        "score1",
        "score2"
    ),
    show="headings"
)

matchesTable.heading("match_id", text="ID")
matchesTable.heading("date", text="Date")
matchesTable.heading("stadium", text="Stadium")
matchesTable.heading("team1", text="Team 1")
matchesTable.heading("team2", text="Team 2")
matchesTable.heading("score1", text="Score 1")
matchesTable.heading("score2", text="Score 2")

matchesTable.column("match_id", width=40)
matchesTable.column("date", width=110)
matchesTable.column("stadium", width=150)
matchesTable.column("team1", width=160)
matchesTable.column("team2", width=160)
matchesTable.column("score1", width=70)
matchesTable.column("score2", width=70)

matchesTable.pack(fill="both",expand=True,padx=20,pady=20)

def loadMatches():
    for row in matchesTable.get_children():
        matchesTable.delete(row)
    c.execute("""
        SELECT
            matches.match_id,
            matches.match_date,
            matches.stadium,
            team1.name,
            team2.name,
            matches.score_t1,
            matches.score_t2
        FROM matches
        JOIN teams AS team1
            ON matches.team_id1 = team1.team_id
        JOIN teams AS team2
            ON matches.team_id2 = team2.team_id
    """)

    matches = c.fetchall()

    for match in matches:
        matchesTable.insert("", "end", values=match)


#select/update functionality for matches
def selectMatch(event):
    selected = matchesTable.selection()
    if selected:
        match = matchesTable.item(selected[0])["values"]

        matchDateEntry.delete(0, "end")
        stadiumEntry.delete(0, "end")
        score1Entry.delete(0, "end")
        score2Entry.delete(0, "end")
        matchDateEntry.insert(0, match[1])
        stadiumEntry.insert(0, match[2])
        team1.set(match[3])
        team2.set(match[4])
        score1Entry.insert(0, match[5])
        score2Entry.insert(0, match[6])

matchesTable.bind("<<TreeviewSelect>>", selectMatch)

# add match
def addMatch():
    selectedTeam1 = team1.get()
    selectedTeam2 = team2.get()

    if not selectedTeam1 or not selectedTeam2:
        messagebox.showwarning("Missing Team","Please select both teams.")
        return

    team_id1 = teamMap[selectedTeam1]
    team_id2 = teamMap[selectedTeam2]
    date = matchDateEntry.get()
    stadium = stadiumEntry.get()
    score1 = score1Entry.get()
    score2 = score2Entry.get()

    c.execute("""
        INSERT INTO matches
        (match_date, stadium, team_id1, team_id2, score_t1, score_t2)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        date,
        stadium,
        team_id1,
        team_id2,
        score1,
        score2
    ))

    conn.commit()

    clearMatchForm()

    loadMatches()
    matchesTable.update()

## update
def updateMatch():
    selected = matchesTable.selection()
    if not selected:
        messagebox.showwarning("Warning","Please select a match to update.")
        return

    match = matchesTable.item(selected[0])["values"]
    match_id = match[0]

    team_id1 = teamMap[team1.get()]
    team_id2 = teamMap[team2.get()]

    c.execute("""
        UPDATE matches
        SET match_date = ?,
            stadium = ?,
            team_id1 = ?,
            team_id2 = ?,
            score_t1 = ?,
            score_t2 = ?
        WHERE match_id = ?
    """, (
        matchDateEntry.get(),
        stadiumEntry.get(),
        team_id1,
        team_id2,
        score1Entry.get(),
        score2Entry.get(),
        match_id
    ))

    conn.commit()

    clearMatchForm()

    loadMatches()
    matchesTable.update()

# delete matches
def deleteMatch():
    selected = matchesTable.selection()
    if not selected:
        messagebox.showwarning("Warning","Please select a match to delete.")
        return

    match = matchesTable.item(selected[0])["values"]
    match_id = match[0]

    c.execute("""
        DELETE FROM matches
        WHERE match_id = ?
    """, (match_id,))

    conn.commit()

    clearMatchForm()

    loadMatches()
    matchesTable.update()

## clear matches form
def clearMatchForm():

    matchDateEntry.delete(0, "end")
    stadiumEntry.delete(0, "end")
    score1Entry.delete(0, "end")
    score2Entry.delete(0, "end")

    team1.set("")
    team2.set("")
# buttons
matchesButton = ttk.Button(matchesForm, text="Add Match", command=addMatch)
matchesButton.grid(column=0, row=6, padx=5, pady=10)
matchesTable.bind("<<TreeviewSelect>>", selectMatch)

updateMatchButton = ttk.Button(matchesForm,text="Update Match",command=updateMatch)
updateMatchButton.grid(column=1, row=6, padx=5, pady=10)

deleteMatchButton = ttk.Button(matchesForm,text="Delete Match",command=deleteMatch)
deleteMatchButton.grid(column=2, row=6, padx=5, pady=10)

################################################################################
# search tab
searchForm = ttk.Frame(searchTab)
searchForm.pack(pady=20)

ttk.Label(searchForm,text="Search:").grid(column=0, row=0, padx=5, pady=5)
searchEntry = ttk.Entry(searchForm, width=30)
searchEntry.grid(column=1, row=0, padx=5, pady=5)

#table
searchTable = ttk.Treeview(
    searchTab,
    columns=(
        "match_id",
        "date",
        "stadium",
        "team1",
        "team2",
        "score1",
        "score2"
    ),
    show="headings"
)

searchTable.heading("match_id", text="ID")
searchTable.heading("date", text="Date")
searchTable.heading("stadium", text="Stadium")
searchTable.heading("team1", text="Team 1")
searchTable.heading("team2", text="Team 2")
searchTable.heading("score1", text="Score 1")
searchTable.heading("score2", text="Score 2")

searchTable.column("match_id", width=40)
searchTable.column("date", width=110)
searchTable.column("stadium", width=150)
searchTable.column("team1", width=160)
searchTable.column("team2", width=160)
searchTable.column("score1", width=70)
searchTable.column("score2", width=70)

searchTable.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


#clear results
def clearSearch():
    for row in searchTable.get_children():
        searchTable.delete(row)

#team search
def searchByTeam():
    clearSearch()
    search = searchEntry.get()

    c.execute("""
        SELECT
            matches.match_id,
            matches.match_date,
            matches.stadium,
            team1.name,
            team2.name,
            matches.score_t1,
            matches.score_t2
        FROM matches
        JOIN teams AS team1
            ON matches.team_id1 = team1.team_id
        JOIN teams AS team2
            ON matches.team_id2 = team2.team_id
        WHERE team1.name LIKE ?
           OR team2.name LIKE ?
    """, (
        "%" + search + "%",
        "%" + search + "%"
    ))

    results = c.fetchall()

    for result in results:
        searchTable.insert("", "end", values=result)


#player search
def searchByPlayer():
    clearSearch()
    search = searchEntry.get()

    c.execute("""
        SELECT DISTINCT
            matches.match_id,
            matches.match_date,
            matches.stadium,
            team1.name,
            team2.name,
            matches.score_t1,
            matches.score_t2
        FROM matches

        JOIN teams AS team1
            ON matches.team_id1 = team1.team_id

        JOIN teams AS team2
            ON matches.team_id2 = team2.team_id

        JOIN players
            ON players.team_id = team1.team_id
            OR players.team_id = team2.team_id

        WHERE players.name LIKE ?
    """, ("%" + search + "%",))

    results = c.fetchall()

    for result in results:
        searchTable.insert("", "end", values=result)


# buttons
searchButtonFrame = ttk.Frame(searchTab)
searchButtonFrame.pack(pady=10)

searchTeamButton = ttk.Button(searchButtonFrame,text="Search by Team",command=searchByTeam)
searchTeamButton.pack(side="left", padx=10)

searchPlayerButton = ttk.Button(searchButtonFrame,text="Search by Player",command=searchByPlayer)
searchPlayerButton.pack(side="left", padx=10)

# Initial match display
loadTeams()
loadMatches()
loadPlayers()
root.mainloop()

