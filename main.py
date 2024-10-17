import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import psycopg2

# Store currently added players for this session
current_players = []

def open_player_entry():
    global red_team_frame, green_team_frame  # Declare frames as global to access in other functions

    splash_screen.destroy()
    # Define connection parameters
    connection_params = {
        'dbname': 'photon',
        'user': 'student',
        #'password': 'student',
        #'host': 'localhost',
        #'port': '5432'
    }

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        # Execute a query
        cursor.execute("SELECT version();")

        # Fetch and display the result
        version = cursor.fetchone()
        print(f"Connected to - {version}")

        # Insert sample data
        cursor.execute('''
            INSERT INTO players (id, codename)
            VALUES (%s, %s);
        ''', ('500', 'BhodiLi'))
        cursor.execute('''
            INSERT INTO players (id, codename)
            VALUES (%s, %s);
        ''', ('232', 'Spark'))
       
        # Commit the changes
        conn.commit()

        # Fetch and display data from the table
        cursor.execute("SELECT * FROM players;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    # Create main player entry window
    player_entry = tk.Tk()
    player_entry.title("Player Entry Screen")
    player_entry.configure(background="black")
    player_entry.geometry("800x600")

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

    # Add Player Button
    add_player_button = tk.Button(
        player_entry, text="Add Player", font=("Arial", 12), bg="darkgreen", fg="white",
        command=lambda: search_or_add_player(id_entry.get(), red_team_frame, green_team_frame)
    )
    add_player_button.grid(row=4, column=0, columnspan=2, pady=10)

    player_entry.bind("<F12>", lambda event: clear_player_entries())

    player_entry.mainloop()

def search_or_add_player(player_id, red_team_frame, green_team_frame):
    connection_params = {
        'dbname': 'photon',
        'user': 'student',
    }

    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        # Search for the player by ID in the database
        cursor.execute("SELECT id, codename FROM players WHERE id = %s;", (player_id,))
        player = cursor.fetchone()

        if player:
            # If found, display the player in the appropriate frame
            current_players.append(player)
        else:
            # If not found, prompt for codename
            codename = simpledialog.askstring("Input", "Enter a codename for the new player:")
            if codename:
                cursor.execute("INSERT INTO players (id, codename) VALUES (%s, %s);", (player_id, codename))
                conn.commit()
                current_players.append((player_id, codename))

        populate_players(red_team_frame, green_team_frame)

    except Exception as error:
        print(f"Error connecting to PostgreSQL database: {error}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def populate_players(red_team_frame, green_team_frame):
    # Clear the frames before repopulating
    for widget in red_team_frame.winfo_children():
        widget.destroy()
    for widget in green_team_frame.winfo_children():
        widget.destroy()

    # Divide the players into red and green teams
    red_team = current_players[:15]
    green_team = current_players[15:]

    # Display Red Team Players
    for i, player in enumerate(red_team):
        player_label = tk.Label(
            red_team_frame,
            text=f"ID: {player[0]}, Codename: {player[1]}",
            bg="darkred", fg="white", font=("Arial", 12)
        )
        player_label.grid(row=i, column=0, sticky="ew", padx=5, pady=2)

    # Display Green Team Players
    for i, player in enumerate(green_team):
        player_label = tk.Label(
            green_team_frame,
            text=f"ID: {player[0]}, Codename: {player[1]}",
            bg="darkgreen", fg="white", font=("Arial", 12)
        )
        player_label.grid(row=i, column=0, sticky="ew", padx=5, pady=2)

# Splash Screen Setup
splash_screen = tk.Tk()
splash_screen.title("Splash Screen")
splash_screen.configure(background="black")
splash_screen.geometry("800x600")

# Load and display splash screen image
image = Image.open("logo.jpg")
image = image.resize((800, 600), Image.LANCZOS)
logo = ImageTk.PhotoImage(image)

logo_label = tk.Label(splash_screen, image=logo)
logo_label.pack()

# Display splash screen for 3 seconds, then show player entry screen
splash_screen.after(3000, open_player_entry)

splash_screen.mainloop()
