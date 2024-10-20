import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import psycopg2
import UDP_Client
import GameActionScreen
from GameActionScreen import openGameActionScreen

# Store currently added players for this session
current_players = []

# Store dynamically created player entries for clearing them later
player_entries = []

def open_player_entry():
    global red_team_frame, green_team_frame, countdown_label  # Declare variables as global for access

    splash_screen.destroy()
    
    connection_params = {
        'dbname': 'photon',
        'user': 'student',
    }

    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Connected to - {version}")
        
        conn.commit()
        
        cursor.execute("SELECT * FROM players;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Create main player entry window
    player_entry = tk.Tk()
    player_entry.title("Player Entry Screen")
    player_entry.configure(background="black")
    player_entry.geometry("800x700")

    # Team Labels
    red_team_label = tk.Label(player_entry, text="RED TEAM", bg="darkred", fg="white", font=("Arial", 16))
    red_team_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    green_team_label = tk.Label(player_entry, text="GREEN TEAM", bg="darkgreen", fg="white", font=("Arial", 16))
    green_team_label.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

    # Frames for Red and Green Teams
    red_team_frame = tk.Frame(player_entry, bg="darkred")
    red_team_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    green_team_frame = tk.Frame(player_entry, bg="darkgreen")
    green_team_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # Player ID Input
    id_label = tk.Label(player_entry, text="Enter Player ID:", bg="black", fg="white", font=("Arial", 12))
    id_label.grid(row=2, column=0, columnspan=2, pady=5)

    id_entry = tk.Entry(player_entry, font=("Arial", 12), width=20)
    id_entry.grid(row=3, column=0, columnspan=2, pady=5)
    player_entries.append(id_entry)

    # Add Player Button
    add_player_button = tk.Button(
        player_entry, text="Add Player", font=("Arial", 12), bg="black", fg="white",
        command=lambda: search_or_add_player(id_entry.get(), red_team_frame, green_team_frame)
    )
    add_player_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Countdown Timer Label (Initially Hidden)
    countdown_label = tk.Label(player_entry, text="", bg="black", fg="white", font=("Arial", 20))
    countdown_label.grid(row=5, column=0, columnspan=2, pady=10)

    # Bind F12 to clear entries and Fn + F5 to start the countdown
    player_entry.bind("<F12>", lambda event: clear_player_entries())
    player_entry.bind("<F5>", lambda event: start_countdown(30))  # Start a 30-second countdown
    # When pressing the F5 key, call the openGameActionScreen() method
     

    populate_players(red_team_frame, green_team_frame)

    player_entry.mainloop()

def start_countdown(seconds):
    """30-second countdown timer in a separate window."""
    # Create a new window for the countdown
    countdown_window = tk.Toplevel()
    countdown_window.title("Countdown Timer")
    countdown_window.geometry("500x300")
    countdown_window.configure(background="black")

    # Label to display the countdown timer
    timer_label = tk.Label(countdown_window, text="", bg="black", fg="white", font=("Arial", 20))
    timer_label.pack(expand=True, padx=20, pady=20)

    def countdown():
        nonlocal seconds
        if seconds > 0:
            timer_label.config(text=f"Time Remaining: {seconds} seconds")
            seconds -= 1
            timer_label.after(1000, countdown)  # Continue countdown every second
        else:
            timer_label.config(text="Game is about to begin!")
            countdown_window.after(1000, lambda: [countdown_window.destroy(), openGameActionScreen(current_players)])  # Close the window and open the game screen

    countdown()  # Start the countdown



def search_or_add_player(player_id, red_team_frame, green_team_frame):
    connection_params = {
        'dbname': 'photon',
        'user': 'student',
    }

    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute("SELECT id, codename FROM players WHERE id = %s;", (player_id,))
        player = cursor.fetchone()

        if player:
            current_players.append(player)
        else:
            codename = simpledialog.askstring("Input", "Enter a codename for the new player:")
            if codename:
                cursor.execute("INSERT INTO players (id, codename) VALUES (%s, %s);", (player_id, codename))
                conn.commit()
                current_players.append((player_id, codename))
                UDP_Client.passInfo(player_id, codename, 1)

        populate_players(red_team_frame, green_team_frame)

    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def populate_players(red_team_frame, green_team_frame):
    for widget in red_team_frame.winfo_children():
        widget.destroy()
    for widget in green_team_frame.winfo_children():
        widget.destroy()

    for i in range(15):
        if i < len(current_players[:15]):
            player = current_players[i]
            text = f"ID: {player[0]}  Codename: {player[1]}  EquipNum: ---"
        else:
            text = "ID: ---  Codename: ---  EquipNum: ---"

        red_player_label = tk.Label(
            red_team_frame, text=text, bg="darkred", fg="white", font=("Arial", 12)
        )
        red_player_label.grid(row=i, column=0, sticky="ew", padx=5, pady=2)

        if i < len(current_players[15:]):
            player = current_players[15 + i]
            text = f"ID: {player[0]}  Codename: {player[1]}  EquipNum: ---"
        else:
            text = "ID: ---  Codename: ---  EquipNum: ---"

        green_player_label = tk.Label(
            green_team_frame, text=text, bg="darkgreen", fg="white", font=("Arial", 12)
        )
        green_player_label.grid(row=i, column=0, sticky="ew", padx=5, pady=2)

    red_team_frame.grid_rowconfigure(list(range(15)), weight=1)
    green_team_frame.grid_rowconfigure(list(range(15)), weight=1)
    red_team_frame.grid_columnconfigure(0, weight=1)
    green_team_frame.grid_columnconfigure(0, weight=1)

def clear_player_entries():
    for entry in player_entries:
        entry.delete(0, 'end')

splash_screen = tk.Tk()
splash_screen.title("Splash Screen")
splash_screen.configure(background="black")
splash_screen.geometry("800x600")

image = Image.open("logo.jpg")
image = image.resize((800, 600), Image.LANCZOS)
logo = ImageTk.PhotoImage(image)

logo_label = tk.Label(splash_screen, image=logo)
logo_label.pack()

splash_screen.after(3000, open_player_entry)
splash_screen.mainloop()
