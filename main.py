
# display a splash screen for 3 seconds 
# then move to a player entry screen 

import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk

# splash screen -> player entry
def open_player_entry():
    splash_screen.destroy()
    
    # Create window
    player_entry = tk.Tk()
    player_entry.title("Player Entry Screen")
    player_entry.configure(background="black")
    
    # size of the window
    player_entry.geometry("800x600")
    
    # 2 columns for teams
    for i in range(2):
        player_entry.columnconfigure(i, weight=2)
    
    # Red Label
    red_team_label = tk.Label(player_entry, text="RED TEAM", bg="darkred", fg="white", font=("Arial", 16,))
    red_team_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    
    # Green Label
    green_team_label = tk.Label(player_entry, text="GREEN TEAM", bg="darkgreen", fg="white", font=("Arial", 16))
    green_team_label.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

    # Frame red  
    red_team_frame = tk.Frame(player_entry, bg="darkred")
    red_team_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    # Frame green  
    green_team_frame = tk.Frame(player_entry, bg="darkgreen")
    green_team_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    
    # Red players
    for i in range(19):
        player_label = tk.Label(red_team_frame, text=f"{i+1}", bg="darkred", fg="white", font=("Arial", 12))
        player_label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
        
        player_entry = tk.Entry(red_team_frame, font=("Arial", 12), width=20)
        player_entry.grid(row=i, column=1, padx=5, pady=2)

        player_entry = tk.Entry(red_team_frame, font=("Arial", 12), width=20)
        player_entry.grid(row=i, column=2, padx=5, pady=2)

        

    # Green players
    for i in range(19):
        player_label = tk.Label(green_team_frame, text=f"{i+1}", bg="darkgreen", fg="white", font=("Arial", 12))
        player_label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
        
        player_entry = tk.Entry(green_team_frame, font=("Arial", 12), width=20)
        player_entry.grid(row=i, column=1, padx=5, pady=2)

        player_entry = tk.Entry(green_team_frame, font=("Arial", 12), width=20)
        player_entry.grid(row=i, column=2, padx=5, pady=2)

    player_entry.mainloop()

# splash screen window
splash_screen = tk.Tk()
splash_screen.title("Splash Screen")
splash_screen.configure(background="black")

# size of window
splash_screen.geometry("800x600")

# splash screen image
# image = Image.open("C:/Users/shane/Desktop/logo.jpg") 
image = Image.open("logo.jpg")
# once github created -> "images\logo.jpg"
logo = ImageTk.PhotoImage(image)
logo_label = tk.Label(splash_screen, image=logo)
logo_label.pack()

# displayed for 3 seconds, then show player entry screen
splash_screen.after(3000, open_player_entry)

splash_screen.mainloop()
