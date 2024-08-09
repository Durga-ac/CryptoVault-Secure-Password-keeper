import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, font
import sqlite3
from cryptography.fernet import Fernet
import os

from password_keeper import PasswordKeeper


class LoginPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login Page")
        self.root.configure(bg="#e4bb6e")  # Set background color
        self.root.iconbitmap("Images/crypto.ico")

        # Set window width and height
        self.window_width = 600
        self.window_height = 500

        # Set font
        self.custom_font_title = font.Font(family="Times New Roman", size=36, weight="bold")
        self.custom_font_label = font.Font(family="Times New Roman", size=24)
        self.custom_font_button = font.Font(family="Times New Roman", size=20, weight="bold")

        # Connect to the database
        self.conn = sqlite3.connect('registryUsers.db')
        self.cur = self.conn.cursor()

        # Center the window
        self.center_window()

        # Title label
        self.label_title = Label(self.root, text="Login", bg="#e4bb6e", font=self.custom_font_title)
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

        # Login button
        self.btn_login = Button(self.root, text="Login", command=self.login, font=self.custom_font_button, bg="#908d87", fg="white", activebackground="#736e64", borderwidth=5, relief=tk.RAISED, padx=20, pady=10)
        self.btn_login.pack(pady=20)
        self.btn_login.image = tk.PhotoImage(file="Images/login.png")  # Replace "Images/login_icon.png" with your image file
        self.btn_login.config(compound=tk.LEFT, image=self.btn_login.image)

        # Signup link
        self.label_signup = Label(self.root, text="Don't have an account? Sign Up", bg="#e4bb6e", fg="blue", font=self.custom_font_button, cursor="hand2")
        self.label_signup.pack(pady=10)
        self.label_signup.bind("<Button-1>", self.open_signup_page)

    def center_window(self):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates for the Tkinter window to be centered
        x_coordinate = (screen_width - self.window_width) // 2
        y_coordinate = (screen_height - self.window_height) // 2

        # Set the position and size of the window
        self.root.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_coordinate, y_coordinate))

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Validate username and password
        if not username.strip() or not password.strip():
            messagebox.showerror("Error", "Username and password are required.")
            return

        try:
            # Check if table exists
            self.cur.execute("SELECT * FROM Users")
            self.cur.fetchone()  # Try fetching a row, if the table doesn't exist, it will raise an exception
        except sqlite3.OperationalError as e:
            messagebox.showerror("Error", "Username not found.")
            return

        # Check if username exists
        self.cur.execute("SELECT * FROM Users WHERE username=?", (username,))
        user = self.cur.fetchone()
        if not user:
            messagebox.showerror("Error", "Username not found.")
            return

        # Decrypt the stored password and check if it matches
        key = user[2]
        cipher_suite = Fernet(key)
        stored_password = user[3].encode()
        decrypted_password = cipher_suite.decrypt(stored_password).decode()

        if password == decrypted_password:
            messagebox.showinfo("Success", "Login successful!")
            # Close the current window
            self.root.destroy()
            # Open the password keeper page with the username
            password_keeper = PasswordKeeper(username)
            password_keeper.run()
        else:
            messagebox.showerror("Error", "Incorrect password!")

    def open_signup_page(self, event):
        # Close the current window and open the signup page
        self.root.destroy()
        os.system("python signup_page.py")

    def run(self):
        self.root.mainloop()

# Create an instance of LoginPage and run the application
if __name__ == "__main__":
    login_page = LoginPage()
    login_page.run()
