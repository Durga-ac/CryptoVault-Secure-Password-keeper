import tkinter as tk
from tkinter import Button, Label, font, PhotoImage
import os

from delete_password import DeletePassword
from search_password import SearchPassword
from store_password import StorePassword
from update_password import UpdatePassword
from view_details import ViewDetails


class PasswordKeeper:
    def __init__(self, username):
        self.username = username  # Store the username passed from the login page

        self.root = tk.Tk()
        self.root.title("Password Keeper")
        self.root.iconbitmap("Images/crypto.ico")

        # Set window width and height
        self.window_width = 700
        self.window_height = 650

        # Load and display background image
        self.background_image = tk.PhotoImage(file="Images/background_1.png")
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.canvas.pack()

        # Title label with background image
        self.label_background_image = tk.PhotoImage(file="Images/background_2.png")
        self.label_title = Label(self.root, image=self.label_background_image, text=f"Hello, {self.username}",
                                 compound=tk.CENTER, font=("Times New Roman", 30, "bold"), borderwidth=0)
        self.label_title.place(relx=0.5, rely=0.17, anchor=tk.CENTER)

        # Button width and height
        button_width = 15
        button_height = 2

        # Button font size
        button_font_size = 18

        # Buttons
        self.button1 = tk.Button(self.root, text="Add Password", font=("Times New Roman", button_font_size),
                                 bg="#908d87", fg="white", width=button_width, height=button_height, padx=15,
                                 command=self.open_store_password)
        self.button1.place(relx=0.5, rely=0.34, anchor=tk.CENTER)

        self.button2 = tk.Button(self.root, text="Update Password", font=("Times New Roman", button_font_size),
                                 bg="#908d87", fg="white", width=button_width, height=button_height, padx=15,
                                 command=self.open_update_password_details)
        self.button2.place(relx=0.5, rely=0.47, anchor=tk.CENTER)

        self.button3 = tk.Button(self.root, text="View Password Details", font=("Times New Roman", button_font_size),
                                 bg="#908d87", fg="white", width=button_width, height=button_height, padx=15,
                                 command=self.open_view_password_details)
        self.button3.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.button4 = tk.Button(self.root, text="Search Password", font=("Times New Roman", button_font_size),
                                 bg="#908d87", fg="white", width=button_width, height=button_height, padx=15,
                                 command=self.open_search_password_details)
        self.button4.place(relx=0.5, rely=0.73, anchor=tk.CENTER)

        self.button5 = tk.Button(self.root, text="Delete Password", font=("Times New Roman", button_font_size),
                                 bg="#908d87", fg="white", width=button_width, height=button_height, padx=15,
                                 command=self.open_delete_password_details)
        self.button5.place(relx=0.5, rely=0.86, anchor=tk.CENTER)

        # Add other buttons as needed

        # Load logout button image
        self.logout_image = tk.PhotoImage(file="Images/logout_button.png")

        # Create a logout button
        self.logout_button = Button(self.root, image=self.logout_image, borderwidth=0, highlightthickness=0,
                                    command=self.goto_login)
        self.logout_button.place(relx=0.795, rely=0.14, anchor=tk.NW)

    def center_window(self):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates for the Tkinter window to be centered
        x_coordinate = (screen_width - self.window_width) // 2
        y_coordinate = (screen_height - self.window_height) // 2

        # Set the position and size of the window
        self.root.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_coordinate, y_coordinate))

    def goto_login(self):
        # Close the current window
        self.root.destroy()
        # Open login_page.py
        os.system("python login_page.py")

    def open_store_password(self):
        # Close the current window
        self.root.destroy()
        # Open store_password.py with the username parameter
        store_password = StorePassword(self.username)
        store_password.run()

    def open_update_password_details(self):
        # Close the current window
        self.root.destroy()
        # Open update_password.py with the username parameter
        update_password = UpdatePassword(self.username)
        update_password.run()

    def open_view_password_details(self):
        # Close the current window
        self.root.destroy()
        # Open view_details.py with the username parameter
        view_details = ViewDetails(self.username)
        view_details.run()

    def open_search_password_details(self):
        # Close the current window
        self.root.destroy()
        # Open view_details.py with the username parameter
        search_password_page = SearchPassword(self.username)
        search_password_page.run()

    def open_delete_password_details(self):
        # Close the current window
        self.root.destroy()
        # Open view_details.py with the username parameter
        delete_password_page = DeletePassword(self.username)
        delete_password_page.run()

    def run(self):
        self.root.mainloop()
