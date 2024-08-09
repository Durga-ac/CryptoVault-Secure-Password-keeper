import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, font, PhotoImage
import sqlite3
from cryptography.fernet import Fernet
import os



class StorePassword:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"Store Password - {self.username}")
        self.root.configure(bg="#e4bb6e")  # Set background color
        self.root.iconbitmap("Images/crypto.ico")

        # Set window width and height
        self.window_width = 700
        self.window_height = 550

        # Set font
        self.custom_font_label = font.Font(family="Times New Roman", size=20)
        self.custom_font_button = font.Font(family="Times New Roman", size=18, weight="bold")

        # Connect to the database
        self.conn = sqlite3.connect('registryUsers.db')
        self.cur = self.conn.cursor()

        # Center the window
        self.center_window()

        # Title label
        self.label_title = Label(self.root, text=f"{self.username}\nStore your password securely", font=("Times New Roman", 30, "bold"), bg="#e4bb6e")
        self.label_title.pack(pady=20)

        # Website label and entry
        self.frame_website = tk.Frame(self.root, bg="#e4bb6e")
        self.frame_website.pack(pady=10)
        self.label_website = Label(self.frame_website, text="Website/App URL:", font=self.custom_font_label, bg="#e4bb6e")
        self.label_website.pack(side=tk.LEFT, padx=10)
        self.entry_website = Entry(self.frame_website, font=self.custom_font_label)
        self.entry_website.pack(side=tk.RIGHT, padx=10, ipady=10, ipadx=20)

        # Password label and entry
        self.frame_password = tk.Frame(self.root, bg="#e4bb6e")
        self.frame_password.pack(pady=10)
        self.label_password = Label(self.frame_password, text="Website/App Password:", font=self.custom_font_label, bg="#e4bb6e")
        self.label_password.pack(side=tk.LEFT, padx=10)
        self.entry_password = Entry(self.frame_password, show="*", font=self.custom_font_label)
        self.entry_password.pack(side=tk.RIGHT, padx=10, ipady=10, ipadx=20)

        # Email label and entry
        self.frame_email = tk.Frame(self.root, bg="#e4bb6e")
        self.frame_email.pack(pady=10)
        self.label_email = Label(self.frame_email, text="Email:", font=self.custom_font_label, bg="#e4bb6e")
        self.label_email.pack(side=tk.LEFT, padx=10)
        self.entry_email = Entry(self.frame_email, font=self.custom_font_label)
        self.entry_email.pack(side=tk.RIGHT, padx=10, ipady=10, ipadx=20)

        # Extra information label and entry
        self.frame_extra = tk.Frame(self.root, bg="#e4bb6e")
        self.frame_extra.pack(pady=10)
        self.label_extra = Label(self.frame_extra, text="Extra Information:", font=self.custom_font_label, bg="#e4bb6e")
        self.label_extra.pack(side=tk.LEFT, padx=10)
        self.entry_extra = Entry(self.frame_extra, font=self.custom_font_label)
        self.entry_extra.pack(side=tk.RIGHT, padx=10, ipady=10, ipadx=20)

        # Save button
        self.btn_save = Button(self.root, text="Save", command=self.save_password, font=self.custom_font_button, bg="#908d87", fg="white", activebackground="#736e64", borderwidth=5, relief=tk.RAISED, padx=20, pady=10)
        self.btn_save.pack(pady=20)

        # Back button
        self.back_image = PhotoImage(file="Images/back_button.png")  # Replace "Images/back_button.png" with your image file
        self.btn_back = Button(self.root, image=self.back_image, borderwidth=0, highlightthickness=0, command=self.go_back)
        self.btn_back.place(x=20, y=20)

    def center_window(self):
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the x and y coordinates for the Tkinter window to be centered
        x_coordinate = (screen_width - self.window_width) // 2
        y_coordinate = (screen_height - self.window_height) // 2

        # Set the position and size of the window
        self.root.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_coordinate, y_coordinate))

    def save_password(self):
        website = self.entry_website.get()
        password = self.entry_password.get()
        email = self.entry_email.get()
        extra = self.entry_extra.get()

        # Validate fields
        if not website.strip() or not password.strip() or not email.strip():
            messagebox.showerror("Error", "Website/URL, Password, and Email fields are required.")
            return

        # Encrypt password, email, and extra information
        key = self.get_encryption_key()
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode()).decode()
        encrypted_website = cipher_suite.encrypt(website.encode()).decode()
        encrypted_email = cipher_suite.encrypt(email.encode()).decode()
        encrypted_extra = cipher_suite.encrypt(extra.encode()).decode()

        # Insert new password entry into the database
        self.cur.execute(
            f"CREATE TABLE IF NOT EXISTS {self.username} (id INTEGER PRIMARY KEY, website_app_url TEXT, website_app_password TEXT, email TEXT, info TEXT)")
        self.cur.execute(
            f"INSERT INTO {self.username} (website_app_url, website_app_password, email, info) VALUES (?, ?, ?, ?)",
            (encrypted_website, encrypted_password, encrypted_email, encrypted_extra))
        self.conn.commit()

        messagebox.showinfo("Success", "Password stored successfully.")

    def get_encryption_key(self):
        self.cur.execute("SELECT encryption_key FROM Users WHERE username=?", (self.username,))
        key = self.cur.fetchone()[0]
        return key

    def go_back(self):
        # Close the current window
        self.root.destroy()
        # Import PasswordKeeper here to avoid circular import
        from password_keeper import PasswordKeeper
        # Open password_keeper.py
        password_keeper_back = PasswordKeeper(self.username)
        password_keeper_back.run()

    def run(self):
        self.root.mainloop()

