# gui.py

import tkinter as tk
from tkinter import ttk, PhotoImage
from pet import Pet

from screentime_tracker import track_screentime

import threading
import queue
import time
from queue import Queue

screentime_updates = Queue()

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

tabControl.add(my_profile, text='My Profile')
tabControl.add(timers, text='Timers')
tabControl.add(shops, text='Shops')



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

# Assuming 'track_screentime' function is already defined and imported

# Global variable to hold the current screentime
current_screentime = 0

def start_screentime_tracker_with_input():
    global current_screentime
    # Get the app bundle ID from the entry widget
    app_bundle_id = app_bundle_id_entry.get()
    print(f"Starting screentime tracker for: {app_bundle_id}")

    # Start the screentime tracker in a new thread to avoid freezing the UI
    def screentime_tracking():
        for screentime in track_screentime(0, app_bundle_id, update_interval=1):
            current_screentime = screentime
            screentime_updates.put(current_screentime)
            print("Current screentime:", current_screentime)

    screentime_thread = threading.Thread(target=screentime_tracking)
    screentime_thread.daemon = True  # Ensure the thread will exit when the main program does
    screentime_thread.start()


# App bundle ID input
app_bundle_id_label = tk.Label(root, text="Enter App Bundle ID:")
app_bundle_id_label.pack()

app_bundle_id_entry = tk.Entry(root)
app_bundle_id_entry.pack()

def update_screentime_display():
    try:
        # Try to get the latest screentime value from the queue
        new_screentime = screentime_updates.get_nowait()
        # Convert the screentime from seconds to hours, minutes, and seconds
        hours, remainder = divmod(new_screentime, 3600)
        minutes, seconds = divmod(remainder, 60)
        # Update the screentime label with the new value in the desired format
        screentime_label.config(text=f"Screentime: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    except queue.Empty:
        pass  # No new value in the queue
    finally:
        # Schedule the next update after 1000ms (1 second)
        screentime_label.after(1000, update_screentime_display)


time_limit = 0
# Start the screentime tracker in a separate thread to avoid blocking the GUI
def start_screentime_thread():
    if time_limit > 0:
        screentime_thread = threading.Thread(target=start_screentime_tracker_with_input)
        screentime_thread.daemon = True  # Ensure the thread will exit when the main program does
        screentime_thread.start()

    # Start updating the screentime display
    update_screentime_display()

# Call 'start_screentime_thread' to begin tracking and updating screentime




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
    global time_limit
    time_limit =  int(timer_entry.get())
    print("Timer set to:", time_limit)

    start_button.config(
        state=tk.DISABLED
    )  # Disable the start button to prevent re-starting
    tracker_thread = threading.Thread(
        target=lambda: track_time(total_time), daemon=True
    )
    tracker_thread.start()

    screentime_tracker_thread = threading.Thread(target=start_screentime_tracker_with_input, daemon=True)
    screentime_tracker_thread.start()


# Function to track time and update character state
def track_time(total_time):
    print("")
    start_time = time.time()
    while True:
        elapsed_time = current_screentime
        #elapsed_time = time.time() - start_time
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


label1 = tk.Label(my_profile,text="My profile")


# Start the Tkinter event loop
start_screentime_thread()

root.mainloop()

