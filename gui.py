# gui.py

import tkinter as tk
from tkinter import ttk, PhotoImage
from pet import Pet
import math

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

####
# Gif functionality
from PIL import Image, ImageTk

# Initialize the pet
my_pet = Pet()


# Load pixel art images for each pet state
images = {
    "happy": "zingaeyes.gif",
    "tired": "happytomeh.gif",
    "exhausted": "concernedtosad.gif",
}

# Dashboard Frames
character_frame = tk.Frame(my_profile, borderwidth=2, padx=10, pady=10, relief="groove")
statistics_frame = tk.Frame(
    my_profile, borderwidth=2, padx=10, pady=10, relief="groove"
)
controls_frame = tk.Frame(my_profile, borderwidth=2, padx=10, pady=10, relief="groove")
timer_frame = tk.Frame(timers, borderwidth=2, padx=10, pady=10, relief="groove")

# Arrange frames in a grid
character_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
statistics_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
controls_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
timers.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
timer_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

timer1_frame = tk.Frame(timer_frame, borderwidth=2, padx=10, pady=10, relief="groove")
timer2_frame = tk.Frame(timer_frame, borderwidth=2, padx=10, pady=10, relief="groove")
timer1_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
timer2_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)


tabControl.add(my_profile, text="My Profile")
tabControl.add(timers, text="Timers")
tabControl.add(shops, text="Shops")

# Assuming the rest of your code remains unchanged up to the shops tab setup...

central_shop_frame = tk.Frame(shops, borderwidth=2, relief="groove")
central_shop_frame.pack(side="left", fill="both", expand=True)

right_shop_frame = tk.Frame(shops, borderwidth=2, relief="groove", bg="#C8A2C8")
right_shop_frame.pack(side="left", fill="y")

central_shop_frame.configure(bg="#C8A2C8")
right_shop_frame.configure(bg="#C8A2C8")


# This will be updated by buttons
central_shop_image = PhotoImage(file="pet_base.png")  # Update path
central_shop_image_label = tk.Label(central_shop_frame, image=central_shop_image)
central_shop_image_label.pack()

# Assuming the right_shop_frame is where you want to display the coins
# Create a frame to hold the coin image and the coin value
coin_display_frame = tk.Frame(
    right_shop_frame, bg="#C8A2C8"
)  # Use the same background color as your shop frame
coin_display_frame.pack(pady=10)  # Adjust padding as needed

# Load and resize the coin image
coin_image = PhotoImage(file="coin.png")  # Update with your coin image path
smaller_coin_image = coin_image.subsample(
    10, 10
)  # Adjust the subsample factors as needed

# Create a Label for the smaller coin image and pack it to the left within the frame
coin_image_label = tk.Label(
    coin_display_frame, image=smaller_coin_image, bg="#C8A2C8"
)  # Use the same background color
coin_image_label.pack(side=tk.LEFT, padx=5)  # Adjust padding as needed

# Create a Label for displaying the coin value and pack it to the right of the coin image within the frame
coin_value_label = tk.Label(
    coin_display_frame,
    text=f"Coins: {my_pet.get_coins()}",
    font=("Comic Sans MS", 14, "normal"),
    bg="#C8A2C8",
)  # Update font and background color as needed
coin_value_label.pack(side=tk.LEFT, padx=5)  # Adjust padding as needed


# Update this function to refresh the coin value when needed
def update_coin_display():
    coin_value_label.config(text=f"Coins: {my_pet.get_coins()}")
    coin_value_label.after(1000, update_coin_display)  # Refresh every 1000ms (1 second)


update_coin_display()  # Call this function to start updating the coin display

# Now you can call update_coin_display() whenever you need to update the coin count display


# Function to update the center image
def update_central_shop_image(new_image_path):
    global central_shop_image
    central_shop_image = PhotoImage(file=new_image_path)  # Load the new image
    central_shop_image_label.config(
        image=central_shop_image
    )  # Update the label to display the new image


# Assuming the rest of your code remains unchanged up to the shops tab setup...


# Function to preview item with the pet
def preview_item_with_pet(item_image_path):
    # You can use the pet's current image and overlay the item image on it
    # For simplicity, this example just switches to the item image
    update_central_shop_image(item_image_path)


# Function to buy the selected item
def buy_item(item_name, item_cost):
    # Deduct the item's cost from the pet's coins
    # You'll need to implement the logic for managing the pet's coins
    if my_pet.coins >= item_cost:
        my_pet.coins -= item_cost
        print(
            f"{item_name} purchased for {item_cost} coins. Remaining coins: {my_pet.coins}"
        )
        # Optionally, update the pet's appearance or attributes based on the purchased item
    else:
        print("Not enough coins.")


# Example items (name, image path, cost)
shop_items = [
    ("Chain", "pet_chain.png", 10),
    ("Flower", "pet_flower.png", 15),
    ("Headphones", "pet_headphones.png", 25),
    ("Shoes", "pet_shoes.png", 40),
    ("Sunglasses", "pet_sunglasses.png", 100),
]

def create_styled_button(container, text, command):
    return tk.Button(
        container,
        text=text,
        command=command,
        font=("Comic Sans MS", 12),
        padx=5,
        pady=5,
        bg="#694b7a",
        fg="#694b7a",
        bd=2,
        relief="ridge",
    )

# Add buttons for each item to the right frame
for item in shop_items:
    # Create a preview button for each item with the standard style
    item_button = create_styled_button(
        right_shop_frame, 
        text=f"Preview {item[0]}", 
        command=lambda item=item: preview_item_with_pet(item[1])
    )
    item_button.pack(pady=(5, 0))  # Add some padding above each button

    # Create a buy button for each item with the standard style
    buy_button = create_styled_button(
        right_shop_frame, 
        text=f"Buy {item[0]} for {item[2]} coins", 
        command=lambda item=item: buy_item(item[0], item[2])
    )
    buy_button.pack(pady=(0, 10))  # Add some padding below each button


# The rest of your code...


# Configure column and row weights to make the frames responsive
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

root.configure(bg="#C8A2C8")

# Set the background color for each frame to lilac purple
character_frame.configure(bg="#C8A2C8")
statistics_frame.configure(bg="#C8A2C8")
controls_frame.configure(bg="#C8A2C8")
timer_frame.configure(bg="#C8A2C8")
timer1_frame.configure(bg="#C8A2C8")
timer2_frame.configure(bg="#C8A2C8")


def play_gif(container, gif_path):
    gif = Image.open(gif_path)  # Open the GIF file using PIL

    # Function to update the displayed frame
    def update_frame(frame):
        try:
            gif.seek(frame)  # Move to the next frame of the GIF
            frame_image = ImageTk.PhotoImage(
                gif.convert("RGBA")
            )  # Convert the image to a Tkinter compatible format
            container.configure(image=frame_image)
            container.image = (
                frame_image  # Keep a reference to avoid garbage collection
            )
            frame += 1
            root.after(
                gif.info["duration"], update_frame, frame
            )  # Schedule the next frame update
        except EOFError:
            update_frame(0)  # Loop the animation

    # Start the animation
    update_frame(0)


# Character Frame where the GIF should be displayed
character_label = tk.Label(character_frame)
character_label.pack(expand=True)


# Function to update character's GIF based on its state
def update_character_gif():
    gif_path = images[my_pet.get_state()]  # Get the current state's GIF path
    play_gif(character_label, gif_path)  # Play the GIF


update_character_gif()

# # Resize image so it doesn't blow up the screen lmao
# ## Get the original image
# original_image = images[my_pet.get_state()]

# ## Resize the image
# resized_image = original_image.subsample(2, 2)  # Reduce the size by half

# Character Label
# character_label = tk.Label(character_frame, image=resized_image, font=("Comic Sans MS", 14, "normal"))
# character_label.pack(expand=True)
# Statistics (Example: Label to show screentime)

screentime_label = tk.Label(
    statistics_frame,
    text="s c r e e n t i m e:\n 0 h 0 m",
    font=("Comic Sans MS", 14, "normal"),
    padx=10,
    pady=10,
    bg="#47523a",
)
screentime_label.pack(expand=True)

# Controls for pet name
name_frame = tk.Frame(
    my_profile, borderwidth=2, relief="groove", bg="#C8A2C8", padx=10, pady=10
)
name_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
root.grid_rowconfigure(2, weight=1)

# Label and Entry for pet name
name_label = tk.Label(
    name_frame,
    text="p e t   n a m e:",
    font=("Comic Sans MS", 14, "normal"),
    padx=10,
    pady=10,
    bg="#47523a",
)
name_label.pack(side=tk.LEFT, padx=5)

name_entry = tk.Entry(
    name_frame, bg="#c1b5c7", font=("Comic Sans MS", 14, "normal"), fg="#000000"
)
name_entry.pack(side=tk.LEFT, expand=True, padx=5)


# Function to set pet's name
def set_pet_name():
    pet_name = name_entry.get()
    my_pet.set_name(pet_name)  # Update this method in the Pet class
    name_entry.delete(0, tk.END)  # Clear the entry field
    update_pet_name_display()  # Update the display with the new name


# Button to set pet name
set_name_button = tk.Button(
    name_frame,
    text="s e t   n a m e",
    command=set_pet_name,
    font=("Comic Sans MS", 14, "normal"),
)
set_name_button.pack(side=tk.RIGHT, padx=5)

# Display label for pet's name
pet_name_display = tk.Label(
    character_frame, text="", font=("Comic Sans MS", 14, "normal")
)
pet_name_display.pack(side=tk.BOTTOM)


def update_pet_name_display():
    pet_name_display.config(text=my_pet.get_name(), padx=10, pady=10, bg="#47523a")
    pet_name_display.pack(side=tk.BOTTOM, padx=10, pady=10)


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
    screentime_thread.daemon = (
        True  # Ensure the thread will exit when the main program does
    )
    screentime_thread.start()


# App bundle ID input
app_bundle_id_label = tk.Label(root, text="Enter App Bundle ID:")
app_bundle_id_label.pack()

app_bundle_id_entry = tk.Entry(root)
app_bundle_id_entry.pack()
new_screentime = 0


def update_screentime_display():
    try:
        global new_screentime
        # Try to get the latest screentime value from the queue
        new_screentime = screentime_updates.get_nowait()
        # Convert the screentime from seconds to hours, minutes, and seconds
        hours, remainder = divmod(new_screentime, 3600)
        minutes, seconds = divmod(remainder, 60)
        # Update the screentime label with the new value in the desired format
        screentime_label.config(
            text=f"Screentime: {int(hours)}h {int(minutes)}m {int(seconds)}s"
        )
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
        screentime_thread.daemon = (
            True  # Ensure the thread will exit when the main program does
        )
        screentime_thread.start()

    # Start updating the screentime display
    update_screentime_display()


# Call 'start_screentime_thread' to begin tracking and updating screentime


# Character Label

# Get the original image
clock_img = PhotoImage(file="clock.png")

# Character Label
character_label = tk.Label(
    timers,
    image=clock_img,
    font=("Comic Sans MS", 14, "normal"),
    bg="#C8A2C8",
    padx=10,
    pady=10,
)
character_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

# Timer Input
timer_label = tk.Label(
    timer1_frame,
    text="set time(s):",
    font=("Comic Sans MS", 14, "normal"),
    padx=10,
    pady=10,
    bg="#47523a",
)
timer_label.pack(side=tk.LEFT, padx=5, pady=5)
timer_entry = tk.Entry(
    timer1_frame, bg="#c1b5c7", font=("Comic Sans MS", 14, "normal"), fg="#ffffff"
)
timer_entry.pack(side=tk.LEFT, padx=5, pady=5)


# Start Button
start_button = tk.Button(
    timer1_frame,
    text="timer: START!",
    font=("Comic Sans MS", 14, "normal"),
    padx=10,
    pady=10,
    bg="#47523a",
    bd=0,
    relief="ridge",
    command=lambda: start_timer(int(timer_entry.get())),
)
start_button.pack(pady=10)

# App bundle ID input
app_bundle_id_label = tk.Label(
    timer2_frame,
    text="enter app bundle i.d.:",
    font=("Comic Sans MS", 14, "italic"),
    padx=10,
    pady=10,
    bg="#694b7a",
)
app_bundle_id_label.pack(side=tk.LEFT, padx=5, pady=5)

app_bundle_id_entry = tk.Entry(
    timer2_frame, bg="#c1b5c7", font=("Comic Sans MS", 14, "normal"), fg="#ffffff"
)
app_bundle_id_entry.pack(pady=10)

# # put timer1 and timer2 in timer_frame
# timer1_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
# timer2_frame.pack(side=tk.TOP, fill=tk.X, expand=True)


# Function to start the timer and screentime tracker
def start_timer(total_time):
    global time_limit
    time_limit = int(timer_entry.get())
    print("Timer set to:", time_limit)

    start_button.config(state=tk.DISABLED, relief="raised")
    tracker_thread = threading.Thread(
        target=lambda: track_time(total_time), daemon=True
    )
    tracker_thread.start()

    screentime_tracker_thread = threading.Thread(
        target=start_screentime_tracker_with_input, daemon=True
    )
    screentime_tracker_thread.start()


# Function to track time and update character state
def track_time(total_time):
    while True:

        try:
            # Try to get the latest screentime value from the queue
            elapsed_time = new_screentime
        except queue.Empty:
            # If the queue is empty, use the last known screentime
            elapsed_time = current_screentime

        print("ELAPSED TIME ", elapsed_time)
        print("TIME_LIMIT ", time_limit)

        if elapsed_time >= time_limit:
            update_character_state("exhausted")
            break  # Break the loop if the time limit is reached
        elif elapsed_time >= time_limit / 2:
            update_character_state("tired")

        time.sleep(1)  # Check every second


# Function to update the pet's state based on time
def update_character_state(state):
    print("Updating character state to {state}")
    root.after(0, lambda: character_label.config(image=images[state]))


label1 = tk.Label(my_profile, text="My profile", font=("Comic Sans MS", 14, "normal"))


# Start the Tkinter event loop
start_screentime_thread()

root.mainloop()
