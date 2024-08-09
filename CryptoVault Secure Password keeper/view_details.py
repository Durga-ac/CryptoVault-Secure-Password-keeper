import tkinter as tk
from tkinter import messagebox, font, Button, Scrollbar
import sqlite3
from cryptography.fernet import Fernet

class ViewDetails:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title("Password Details")
        self.root.configure(bg="#e4bb6e")  # Set background color
        self.root.iconbitmap("Images/crypto.ico")

        # Set window width and height
        self.window_width = 600
        self.window_height = 500

        # Set font
        self.custom_font_label = font.Font(family="Times New Roman", size=12)  # Decreased font size

        # Connect to the database
        self.conn = sqlite3.connect('registryUsers.db')
        self.cur = self.conn.cursor()

        # Create a frame to hold the password details
        self.frame = tk.Frame(self.root, bg="#e4bb6e")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Back button
        self.back_image = tk.PhotoImage(file="Images/back_button.png")  # Replace "Images/logout.png" with your image file
        self.btn_back = Button(self.frame, image=self.back_image, borderwidth=0, highlightthickness=0, command=self.go_back)
        self.btn_back.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.NW)  # Aligned to top-left

        # Title label
        self.label_title = tk.Label(self.frame, text="Password Details", font=("Times New Roman", 20, "bold"), bg="#e4bb6e")
        self.label_title.pack(pady=10)

        # Create a scrollable text area for displaying password details
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.password_text = tk.Text(self.frame, font=self.custom_font_label, bg="#e4bb6e", wrap="word", yscrollcommand=self.scrollbar.set)
        self.password_text.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.password_text.yview)

        # Display password details in encrypted form initially
        self.display_password_details(encrypted=True)

        # Decrypt button
        self.btn_decrypt = Button(self.frame, text="Decrypt", font=("Times New Roman", 14), bg="#908d87", fg="white", command=self.decrypt_passwords)
        self.btn_decrypt.pack(pady=10, side=tk.BOTTOM)  # Moved to bottom

    def display_password_details(self, encrypted=True):
        try:
            # Fetch password details from the database
            self.cur.execute(f"SELECT * FROM {self.username}")
            password_entries = self.cur.fetchall()

            # Display password details
            for entry in password_entries:
                id_, website, encrypted_password, email, extra = entry
                decrypted_password = encrypted_password if encrypted else self.decrypt_password(encrypted_password)
                decrypted_website = website if encrypted else self.decrypt_password(website)
                decrypted_email = email if encrypted else self.decrypt_password(email)
                decrypted_extra = extra if encrypted else self.decrypt_password(extra)
                if extra:  # Only display 'Info' field if it's not empty
                    password_text = f"ID: {id_}\nWebsite/URL: {decrypted_website}\nPassword: {decrypted_password}\nEmail: {decrypted_email}\nInfo: {decrypted_extra}\n\n"
                else:
                    password_text = f"ID: {id_}\nWebsite/URL: {decrypted_website}\nPassword: {decrypted_password}\nEmail: {decrypted_email}\n\n"
                self.password_text.insert(tk.END, password_text)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to fetch password details: {e}")

    def decrypt_password(self, encrypted_data):
        try:
            # Fetch encryption key from the database
            self.cur.execute("SELECT encryption_key FROM Users WHERE username=?", (self.username,))
            key = self.cur.fetchone()[0]

            # Decrypt data using Fernet
            cipher_suite = Fernet(key)
            decrypted_data = cipher_suite.decrypt(encrypted_data.encode()).decode()
            return decrypted_data

        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt data: {e}")

    def decrypt_passwords(self):
        # Clear the text area
        self.password_text.delete(1.0, tk.END)

        # Display password details with decrypted passwords
        self.display_password_details(encrypted=False)

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

