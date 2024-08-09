import tkinter as tk
from tkinter import messagebox, font, Checkbutton, Button, Scrollbar
import sqlite3
from cryptography.fernet import Fernet

class DeletePassword:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title("Delete Passwords")
        self.root.configure(bg="#e4bb6e")
        self.root.iconbitmap("Images/crypto.ico")

        # Window dimensions and font settings
        self.window_width = 800
        self.window_height = 500
        self.custom_font_label = font.Font(family="Times New Roman", size=16)

        # Connect to the database
        self.conn = sqlite3.connect('registryUsers.db')
        self.cur = self.conn.cursor()

        # Create a frame to hold the password entries
        self.frame = tk.Frame(self.root, bg="#e4bb6e")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Back button
        self.back_image = tk.PhotoImage(file="Images/back_button.png")  # Replace "Images/logout.png" with your image file
        self.btn_back = Button(self.frame, image=self.back_image, borderwidth=0, highlightthickness=0,
                               command=self.go_back)
        self.btn_back.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.NW)  # Aligned to top-left

        # Title label
        self.label_title = tk.Label(self.frame, text="Delete Passwords", font=("Times New Roman", 20, "bold"), bg="#e4bb6e")
        self.label_title.pack(pady=10)

        # Create a canvas with a scrollbar
        self.canvas = tk.Canvas(self.frame, bg="#e4bb6e", width=self.window_width, height=self.window_height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Frame to contain password entries
        self.password_frame = tk.Frame(self.canvas, bg="#e4bb6e")
        self.canvas.create_window((0, 0), window=self.password_frame, anchor=tk.NW)

        # Display decrypted password details
        self.display_passwords()

        # Buttons for select, delete, and unselect
        self.create_buttons()

    def create_buttons(self):
        # Frame for buttons
        self.button_frame = tk.Frame(self.root, bg="#e4bb6e")
        self.button_frame.pack(pady=10)

        # Select button
        self.btn_select = Button(self.button_frame, text="Select", font=self.custom_font_label, bg="#908d87", fg="white", command=self.enable_checkboxes)
        self.btn_select.pack(side=tk.LEFT, padx=10)

        # Delete button
        self.btn_delete = Button(self.button_frame, text="Delete", font=self.custom_font_label, bg="#908d87", fg="white", state=tk.DISABLED, command=self.delete_passwords)
        self.btn_delete.pack(side=tk.LEFT, padx=10)

        # Unselect button
        self.btn_unselect = Button(self.button_frame, text="Unselect", font=self.custom_font_label, bg="#908d87", fg="white", state=tk.DISABLED, command=self.unselect_checkboxes)
        self.btn_unselect.pack(side=tk.LEFT, padx=10)

    def display_passwords(self):
        try:
            self.cur.execute(f"SELECT * FROM {self.username}")
            password_entries = self.cur.fetchall()

            # Display decrypted password details with checkboxes
            self.checkboxes = []
            for entry in password_entries:
                id_, website, encrypted_password, email, extra = entry
                decrypted_password = self.decrypt_data(encrypted_password)
                decrypted_website = self.decrypt_data(website)
                decrypted_email = self.decrypt_data(email)
                decrypted_extra = self.decrypt_data(extra) if extra else ""

                password_text = f"ID: {id_}\nWebsite/URL: {decrypted_website}\nPassword: {decrypted_password}\nEmail: {decrypted_email}\nInfo: {decrypted_extra}\n"

                # Create a frame for each password entry
                entry_frame = tk.Frame(self.password_frame, bg="#e4bb6e")
                entry_frame.pack(anchor=tk.W, padx=10, pady=10, fill=tk.X)

                # Password details label
                password_label = tk.Label(entry_frame, text=password_text, font=self.custom_font_label, bg="#e4bb6e", width=60)
                password_label.pack(side=tk.LEFT, anchor=tk.W)

                # Checkbox for each entry
                checkbox_var = tk.BooleanVar(value=False)
                checkbox = Checkbutton(entry_frame, variable=checkbox_var, bg="#e4bb6e", state=tk.DISABLED)
                checkbox.pack(side=tk.LEFT, padx=5)

                # Append checkbox to the list
                self.checkboxes.append((checkbox, checkbox_var, id_))

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to fetch password details: {e}")

    def decrypt_data(self, encrypted_data):
        try:
            self.cur.execute("SELECT encryption_key FROM Users WHERE username=?", (self.username,))
            key = self.cur.fetchone()[0]
            cipher_suite = Fernet(key)
            decrypted_data = cipher_suite.decrypt(encrypted_data.encode()).decode()
            return decrypted_data

        except Exception as e:
            messagebox.showerror("Error", f"Failed to decrypt data: {e}")

    def enable_checkboxes(self):
        # Enable checkboxes and buttons
        for checkbox, _, _ in self.checkboxes:
            checkbox.config(state=tk.NORMAL)

        self.btn_delete.config(state=tk.NORMAL)
        self.btn_unselect.config(state=tk.NORMAL)
        self.btn_select.config(state=tk.DISABLED)

    def unselect_checkboxes(self):
        # Uncheck all checkboxes and disable them
        for checkbox, checkbox_var, _ in self.checkboxes:
            checkbox_var.set(False)
            checkbox.config(state=tk.DISABLED)

        self.btn_delete.config(state=tk.DISABLED)
        self.btn_unselect.config(state=tk.DISABLED)
        self.btn_select.config(state=tk.NORMAL)

    def delete_passwords(self):
        # Get IDs of selected passwords
        selected_ids = [id_ for _, checkbox_var, id_ in self.checkboxes if checkbox_var.get()]

        if not selected_ids:
            messagebox.showinfo("No Selection", "Please select passwords to delete.")
            return

        try:
            # Delete selected passwords from the database
            placeholders = ','.join('?' for _ in selected_ids)
            self.cur.execute(f"DELETE FROM {self.username} WHERE id IN ({placeholders})", selected_ids)
            self.conn.commit()
            messagebox.showinfo("Success", "Selected passwords have been deleted.")

            # Refresh the display after deletion
            self.clear_password_frame()
            self.display_passwords()

            # Re-enable the Select button and disable Delete and Unselect buttons
            self.btn_select.config(state=tk.NORMAL)
            self.btn_delete.config(state=tk.DISABLED)
            self.btn_unselect.config(state=tk.DISABLED)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to delete passwords: {e}")

    def clear_password_frame(self):
        # Clear the password frame before refreshing
        for widget in self.password_frame.winfo_children():
            widget.destroy()

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
