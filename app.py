import tkinter as tk
from tkinter import messagebox
import sqlite3
from cryptography.fernet import Fernet
import random
import string

# Generate a Fernet key for encryption
key = Fernet.generate_key()
fernet = Fernet(key)

# Connect to the SQLite database
conn = sqlite3.connect('passwords.db')
cursor = conn.cursor()

# Create the 'passwords' table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                  id INTEGER PRIMARY KEY,
                  website TEXT NOT NULL,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL)''')
conn.commit()

# Function to add a new password
def add_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not website or not username or not password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Encrypt the password before storing it
    encrypted_password = fernet.encrypt(password.encode())

    cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                   (website, username, encrypted_password))
    conn.commit()
    clear_entries()
    display_passwords()
    messagebox.showinfo("Success", "Password added successfully!")

# Function to retrieve and display passwords
def display_passwords():
    passwords_listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM passwords")
    for row in cursor.fetchall():
        website = row[1]
        username = row[2]
        # Decrypt the password for display
        decrypted_password = fernet.decrypt(row[3]).decode()
        passwords_listbox.insert(tk.END, f"Website: {website}, Username: {username}, Password: {decrypted_password}")

# Function to generate a random password
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# Function to clear input fields
def clear_entries():
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Create the Tkinter window
window = tk.Tk()
window.title("PassSentinel")

# Labels
website_label = tk.Label(text="Website:")
website_label.grid(row=0, column=0)
username_label = tk.Label(text="Username:")
username_label.grid(row=1, column=0)
password_label = tk.Label(text="Password:")
password_label.grid(row=2, column=0)

# Entry fields
website_entry = tk.Entry(width=40)
website_entry.grid(row=0, column=1)
username_entry = tk.Entry(width=40)
username_entry.grid(row=1, column=1)
password_entry = tk.Entry(width=40)
password_entry.grid(row=2, column=1)

# Buttons
add_button = tk.Button(text="Add Password", command=add_password)
add_button.grid(row=3, column=1)
generate_button = tk.Button(text="Generate Password", command=generate_password)
generate_button.grid(row=2, column=2)
clear_button = tk.Button(text="Clear Entries", command=clear_entries)
clear_button.grid(row=3, column=0)

# Password list
passwords_listbox = tk.Listbox(width=50)
passwords_listbox.grid(row=4, column=0, columnspan=3)

# Display existing passwords
display_passwords()

window.mainloop()
