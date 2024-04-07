# pet.py

class Pet:
    def __init__(self):
        # Initialize the pet's state
        self.state = "happy"
        self.name = "NetPet"
        self.coins = 15

    def get_state(self):
        # Return the current state
        return self.state
    
    def add_coins(self, num):
        self.coins = self.coins + num

    def get_coins(self):
        return self.coins


    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name




'''
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_width = 100
window_height = 100

# Set the color (RGBA) and transparency level (0-255) for the window background
background_color = (0, 0, 0, 0)  # Transparent background
transparency = 150  # Adjust transparency level as needed

# Create the Pygame window with a transparent background
window = pygame.display.set_mode((window_width, window_height), pygame.SCALED | pygame.NOFRAME)
window.set_alpha(None)  # Enable per-pixel alpha blending
window.set_colorkey((0, 0, 0))  # Set transparent color

# Set the initial position of the window
window_x = 0
window_y = 100

# Main loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the window
    window.fill(background_color)

    # Draw content or interact with the user here

    # Update the display
    pygame.display.flip()

    # Position the window
'''