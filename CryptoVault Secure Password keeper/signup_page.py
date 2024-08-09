import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, font
import sqlite3
from cryptography.fernet import Fernet
import os

class SignupPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Signup Page")
        self.root.configure(bg="#e4bb6e")  # Set background color
        self.root.iconbitmap("Images/crypto.ico")

        # Set window width and height
        self.window_width = 600
        self.window_height = 500

        # Set font
        self.custom_font_title = font.Font(family="Times New Roman", size=36, weight="bold")
        self.custom_font_label = font.Font(family="Times New Roman", size=24)
        self.custom_font_button = font.Font(family="Times New Roman", size=20, weight="bold")

        # Connect to the database and create the Users table if it doesn't exist
        self.conn = sqlite3.connect('registryUsers.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE,
                            encryption_key TEXT,
                            password TEXT
                            )''')
        self.conn.commit()

        # Center the window
        self.center_window()

        # Title label
        self.label_title = Label(self.root, text="Signup", bg="#e4bb6e", font=self.custom_font_title)
        self.label_title.pack(pady=20)

        # Username label and entry
        self.frame_username = tk.Frame(self.root, bg="#e4bb6e")
        self.frame_username.pack(pady=10)
        self.label_username = Label(self.frame_username, text="Username:", bg="#e4bb6e", font=self.custom_font_label)
        self.label_username.pack(side=tk.LEFT, padx=10)
        self.entry_username = Entry(self.frame_username, font=self.custom_font_label)
        self.entry_username.pack(side=tk.RIGHT, padx=10, ipady=10, ipadx=20)

        # Password label and entry
        self.frame_password = tk.Frame(self.root, bg="#e4bb6e")
        self.frame_password.pack(pady=10)
        self.label_password = Label(self.frame_password, text="Password:", bg="#e4bb6e", font=self.custom_font_label)
        self.label_password.pack(side=tk.LEFT, padx=10)
        self.entry_password = Entry(self.frame_password, show="*", font=self.custom_font_label)
        self.entry_password.pack(side=tk.RIGHT, padx=10, ipady=10, ipadx=20)

        # Sign up button
        self.btn_signup = Button(self.root, text="Sign Up", command=self.signup, font=self.custom_font_button, bg="#908d87", fg="white", activebackground="#736e64", borderwidth=5, relief=tk.RAISED, padx=20, pady=10)
        self.btn_signup.pack(pady=20)
        self.btn_signup.image = tk.PhotoImage(file="Images/login.png")  # Replace "Images/signup_icon.png" with your image file
        self.btn_signup.config(compound=tk.LEFT, image=self.btn_signup.image)

        # Login link
        self.label_login = Label(self.root, text="Already have an account? Login", bg="#e4bb6e", fg="blue", font=self.custom_font_button, cursor="hand2")
        self.label_login.pack(pady=10)
        self.label_login.bind("<Button-1>", self.open_login_page)

    def center_window(self):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates for the Tkinter window to be centered
        x_coordinate = (screen_width - self.window_width) // 2
        y_coordinate = (screen_height - self.window_height) // 2

        # Set the position and size of the window
        self.root.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_coordinate, y_coordinate))

    def signup(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if username already exists
        self.cur.execute("SELECT * FROM Users WHERE username=?", (username,))
        user = self.cur.fetchone()
        if user:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            return

        # Validate username and password
        if not username.strip() or not password.strip():
            messagebox.showerror("Error", "Username and password are required.")
            return

        # Generate encryption key and encrypt password
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()

        # Insert new user into database
        self.cur.execute("INSERT INTO Users (username, encryption_key, password) VALUES (?, ?, ?)", (username, key, encrypted_password))  # Store the key directly
        self.conn.commit()

        messagebox.showinfo("Success", "Signup successful!")

        # Close current window
        self.root.destroy()
        # Open login_page.py
        os.system("python login_page.py")

    def open_login_page(self, event):
        # Close the current window and open the login page
        self.root.destroy()
        os.system("python login_page.py")

    def run(self):
        self.root.mainloop()

# Create an instance of SignupPage and run the application
if __name__ == "__main__":
    signup_page = SignupPage()
    signup_page.run()