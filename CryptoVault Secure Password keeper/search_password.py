import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, font, PhotoImage
import sqlite3
from cryptography.fernet import Fernet

class SearchPassword:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"Search Password - {self.username}")
        self.root.configure(bg="#e4bb6e")  # Set background color
        self.root.iconbitmap("Images/crypto.ico")

        # Set window width and height
        self.window_width = 700
        self.window_height = 650

        # Set font
        self.custom_font_label = font.Font(family="Times New Roman", size=20)
        self.custom_font_button = font.Font(family="Times New Roman", size=18, weight="bold")

        # Connect to the database
        self.conn = sqlite3.connect('registryUsers.db')
        self.cur = self.conn.cursor()

        # Center the window
        self.center_window()

        # Title label
        self.label_title = Label(self.root, text=f"{self.username}\nSearch Password", font=("Times New Roman", 30, "bold"), bg="#e4bb6e")
        self.label_title.pack(pady=20)

        # Search label and entry
        self.frame_search = tk.Frame(self.root, bg="#e4bb6e")
        self.frame_search.pack(pady=10)
        self.label_search = Label(self.frame_search, text="Enter ID:", font=self.custom_font_label, bg="#e4bb6e")
        self.label_search.pack(side=tk.LEFT, padx=10)
        self.entry_search = Entry(self.frame_search, font=self.custom_font_label)
        self.entry_search.pack(side=tk.RIGHT, padx=10, ipady=10, ipadx=20)

        # Search button
        self.btn_search = Button(self.root, text="Search", command=self.search_password, font=self.custom_font_button, bg="#908d87", fg="white", activebackground="#736e64", borderwidth=5, relief=tk.RAISED, padx=20, pady=10)
        self.btn_search.pack(pady=20)

        # Result labels
        self.label_website = Label(self.root, text="", font=self.custom_font_label, bg="#e4bb6e")
        self.label_website.pack(pady=10)
        self.label_password = Label(self.root, text="", font=self.custom_font_label, bg="#e4bb6e")
        self.label_password.pack(pady=10)
        self.label_email = Label(self.root, text="", font=self.custom_font_label, bg="#e4bb6e")
        self.label_email.pack(pady=10)
        self.label_extra = Label(self.root, text="", font=self.custom_font_label, bg="#e4bb6e")
        self.label_extra.pack(pady=10)

        # Back button
        self.back_image = PhotoImage(file="Images/back_button.png")  # Replace "Images/logout.png" with your image file
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

    def search_password(self):
        search_term = self.entry_search.get().strip()
        if not search_term:
            messagebox.showerror("Error", "Please enter an ID to search.")
            return

        # Fetch data based on ID
        self.cur.execute(f"SELECT * FROM {self.username} WHERE id=?", (search_term,))
        row = self.cur.fetchone()

        if row:
            _, website, password, email, extra = row

            # Decrypt fetched data
            decrypted_website = self.decrypt_data(website)
            decrypted_password = self.decrypt_data(password)
            decrypted_email = self.decrypt_data(email)
            decrypted_extra = self.decrypt_data(extra)

            # Display decrypted data in result labels
            self.display_result(decrypted_website, decrypted_password, decrypted_email, decrypted_extra)
        else:
            messagebox.showinfo("Not Found", "No entry found with the provided ID.")

    def decrypt_data(self, encrypted_data):
        key = self.get_encryption_key()
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data.encode()).decode()
        return decrypted_data

    def display_result(self, website, password, email, extra):
        self.label_website.config(text=f"Website/App URL: {website}")
        self.label_password.config(text=f"Website/App Password: {password}")
        self.label_email.config(text=f"Email: {email}")
        self.label_extra.config(text=f"Extra Information: {extra}")

    def get_encryption_key(self):
        self.cur.execute("SELECT encryption_key FROM Users WHERE username=?", (self.username,))
        key = self.cur.fetchone()[0]
        return key

    def go_back(self):
        # Close the current window
        self.root.destroy()
        # Import your PasswordKeeper class here
        from password_keeper import PasswordKeeper
        # Open password_keeper.py
        password_keeper_back = PasswordKeeper(self.username)
        password_keeper_back.run()

    def run(self):
        self.root.mainloop()