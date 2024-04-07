# gui.py

import tkinter as tk
from tkinter import ttk, PhotoImage
from pet import Pet

#from screentime_tracker import track_screentime

import threading
import queue
import time

# Initialize the main window
root = tk.Tk()
root.title("Pixel Pet Dashboard")

# Create a notebook for tabs

tabControl = ttk.Notebook(root)
tabControl.pack(fill="both", expand=True)

my_profile = ttk.Frame(tabControl)
timers = ttk.Frame(tabControl)
shops = ttk.Frame(tabControl)

# Initialize the pet
my_pet = Pet()

# Load pixel art images for each pet state
images = {
    "happy": PhotoImage(file="happy.png"),
    "tired": PhotoImage(file="tired.png"),
    "exhausted": PhotoImage(file="exhausted.png"),
}

# Dashboard Frames
character_frame = tk.Frame(my_profile, borderwidth=2, relief="groove")
statistics_frame = tk.Frame(my_profile, borderwidth=2, relief="groove")
controls_frame = tk.Frame(my_profile, borderwidth=2, relief="groove")
timer_frame = tk.Frame(my_profile, borderwidth=2, relief="groove")

# Arrange frames in a grid
character_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
statistics_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
controls_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
timer_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

# Configure column and row weights to make the frames responsive
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

root.configure(bg='#C8A2C8')

# Set the background color for each frame to lilac purple
character_frame.configure(bg='#C8A2C8')
statistics_frame.configure(bg='#C8A2C8')
controls_frame.configure(bg='#C8A2C8')
timer_frame.configure(bg='#C8A2C8')

# Character Label
character_label = tk.Label(character_frame, image=images[my_pet.get_state()])
character_label.pack(expand=True)

# Statistics (Example: Label to show screentime)
screentime_label = tk.Label(statistics_frame, text="Screentime: 0h 0m")
screentime_label.pack(expand=True)


# Controls for pet name
name_frame = tk.Frame(my_profile, borderwidth=2, relief="groove")
name_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
root.grid_rowconfigure(2, weight=1)

# Label and Entry for pet name
name_label = tk.Label(name_frame, text="Pet Name:")
name_label.pack(side=tk.LEFT, padx=5)

name_entry = tk.Entry(name_frame)
name_entry.pack(side=tk.LEFT, expand=True, padx=5)


# Function to set pet's name
def set_pet_name():
    pet_name = name_entry.get()
    my_pet.set_name(pet_name)  # Update this method in the Pet class
    name_entry.delete(0, tk.END)  # Clear the entry field
    update_pet_name_display()  # Update the display with the new name


# Button to set pet name
set_name_button = tk.Button(name_frame, text="Set Name", command=set_pet_name)
set_name_button.pack(side=tk.RIGHT, padx=5)

# Display label for pet's name
pet_name_display = tk.Label(character_frame, text="")
pet_name_display.pack(side=tk.BOTTOM)


def update_pet_name_display():
    pet_name_display.config(text=my_pet.get_name())


update_pet_name_display()

# screentime tracket
screentime_queue = queue.Queue()


def start_screentime_tracker():
    print("start_screentime_tracker running")
    for screentime in track_screentime("com.tinyspeck.slackmacgap"):
        screentime_queue.put(screentime)
        print("screentime running")


# Function to update the screentime label
# Function to update the screentime label with seconds included
def update_screentime_display():
    try:
        # Get the latest screentime value from the queue
        screentime = screentime_queue.get_nowait()
        # Format the screentime into hours, minutes, and seconds and update the label
        hours, remainder = divmod(screentime, 3600)
        minutes, seconds = divmod(remainder, 60)
        screentime_label.config(
            text=f"Screentime: {int(hours)}h {int(minutes)}m {int(seconds)}s"
        )
    except queue.Empty:
        pass
    finally:
        # Schedule this function to be called again after 1000ms (1 second) to keep the display updated
        root.after(1000, update_screentime_display)


# Start the periodic update for the screentime display
update_screentime_display()


# Timer Input
timer_label = tk.Label(timer_frame, text="Set Time (s):")
timer_label.pack(side=tk.LEFT, padx=5, pady=5)
timer_entry = tk.Entry(timer_frame)
timer_entry.pack(side=tk.LEFT, padx=5, pady=5)

# Start Button
start_button = tk.Button(
    timer_frame, text="Start Timer", command=lambda: start_timer(int(timer_entry.get()))
)
start_button.pack(pady=10)


# Function to start the timer and screentime tracker
def start_timer(total_time):
    start_button.config(
        state=tk.DISABLED
    )  # Disable the start button to prevent re-starting
    tracker_thread = threading.Thread(
        target=lambda: track_time(total_time), daemon=True
    )
    tracker_thread.start()

    screentime_tracker_thread = threading.Thread(target=start_screentime_tracker, daemon=True)
    screentime_tracker_thread.start()


# Function to track time and update character state
def track_time(total_time):
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= total_time:
            update_character_state("exhausted")
            break
        elif elapsed_time >= total_time / 2:
            update_character_state("tired")
        time.sleep(1)  # Check every second


# Function to update the pet's state based on time
def update_character_state(state):
    print("Updating character state to {state}")
    root.after(0, lambda: character_label.config(image=images[state]))


"""
# Controls (Example: Buttons to simulate screentime)
btn_increase_screentime = tk.Button(controls_frame, text="Increase Screentime", command=increase_screentime)
btn_increase_screentime.pack(side=tk.LEFT, expand=True)

btn_reset_screentime = tk.Button(controls_frame, text="Reset Screentime", command=reset_screentime)
btn_reset_screentime.pack(side=tk.LEFT, expand=True)

# Event Handlers for Controls
def increase_screentime():
    # This would be a placeholder to simulate increasing screentime
    print("Increase screentime")

def reset_screentime():
    # This would reset the screentime
    print("Reset screentime")
"""


# Update Function (simply call this once for now)
# This would be called periodically in the real application
"""def update_character_state():
    # Update the pet's state and the image shown
    character_label.config(image=images[my_pet.get_state()])
"""


label1 = tk.Label(my_profile,text="My profile")

# Start the Tkinter event loop
root.mainloop()
