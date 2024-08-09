import tkinter as tk
from tkinter import PhotoImage
import pygame
import os

class MainCrypto:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Crypto Main")
        self.root.iconbitmap("Images/crypto.ico")  # Replace "path_to_icon.ico" with the path to your icon file

        # Set window width and height
        self.window_width = 700
        self.window_height = 650

        # Create a canvas to place the background image
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.pack()

        # Load and display image as background
        self.background_image = PhotoImage(file="Images/logo.png")  # Replace "Images/logo.png" with your image file
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        # Center the window and ensure equal margins
        self.center_window()

        # Initialize Pygame mixer
        pygame.mixer.init()

        # Schedule redirect to login page after 10 seconds
        self.root.after(10000, self.redirect_to_login)

    def play_audio(self, audio_file):
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

    def stop_audio(self):
        pygame.mixer.music.stop()

    def center_window(self):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates for the Tkinter window to be centered
        x_coordinate = (screen_width - self.window_width) // 2
        y_coordinate = (screen_height - self.window_height) // 2

        # Set the position and size of the window
        self.root.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_coordinate, y_coordinate))

    def redirect_to_login(self):
        # Stop the music
        self.stop_audio()
        # Close the current window and open the login page
        self.root.destroy()
        os.system("python login_page.py")

    def run(self):
        self.root.mainloop()

# Create an instance of MainCrypto and run the application
if __name__ == "__main__":
    app = MainCrypto()
    app.play_audio("audio/fun.mpeg")  # Load and play audio file immediately
    app.run()
