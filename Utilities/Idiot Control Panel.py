import tkinter as tk
from tkinter import messagebox
import random

# Function to display random error messages
def trigger_error():
    errors = [
        "404: Coffee not found!",
        "Error: Keyboard not connected. Press F1 to continue.",
        "Warning: Your computer might explode. Maybe.",
        "Oops! Something went right!",
        "Blue screen... just kidding!"
    ]
    messagebox.showerror("Critical Error", random.choice(errors))

# Function to make the progress bar do something pointless
def pointless_progress():
    progress = random.randint(0, 100)
    progress_var.set(progress)
    if progress == 100:
        messagebox.showinfo("Progress Complete", "You've wasted enough time!")

# Function to show a fake success message
def fake_success():
    messagebox.showinfo("Success!", "Operation completed successfully! Just kidding.")

# Creating the main window
root = tk.Tk()
root.title("Idiot Control Panel")
root.geometry("300x200")

# Creating a label
label = tk.Label(root, text="Control Panel", font=("Helvetica", 16))
label.pack(pady=10)

# Adding buttons with humorous functions
button1 = tk.Button(root, text="Self-Destruct", command=trigger_error)
button1.pack(pady=5)

button2 = tk.Button(root, text="Pointless Progress", command=pointless_progress)
button2.pack(pady=5)

button3 = tk.Button(root, text="Fake Success", command=fake_success)
button3.pack(pady=5)

# Progress bar that does nothing useful
progress_var = tk.IntVar()
progress_bar = tk.Scale(root, from_=0, to=100, orient="horizontal", variable=progress_var)
progress_bar.pack(pady=10)

# Run the application
root.mainloop()
