import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# Database setup
def setup_database():
	connection = sqlite3.connect("mood_tracker.db")
	cursor = connection.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS mood_logs (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			date TEXT NOT NULL,
			mood TEXT NOT NULL,
			note TEXT
		)
	""")
	connection.commit()
	connection.close()

# Save mood entry to database
def save_mood(date, mood, note):
	connection = sqlite3.connect("mood_tracker.db")
	cursor = connection.cursor()
	cursor.execute("INSERT INTO mood_logs (date, mood, note) VALUES (?, ?, ?)", (date, mood, note))
	connection.commit()
	connection.close()

# Fetch mood data for visualization
def fetch_mood_data():
	connection = sqlite3.connect("mood_tracker.db")
	cursor = connection.cursor()
	cursor.execute("SELECT date, mood FROM mood_logs")
	data = cursor.fetchall()
	connection.close()
	return data

# Plot mood trends
def plot_mood_trends():
	data = fetch_mood_data()
	if not data:
		messagebox.showinfo("No Data", "No mood data available to display trends.")
		return

	dates = [datetime.strptime(row[0], "%Y-%m-%d") for row in data]
	moods = [row[1] for row in data]

	mood_levels = {"Happy": 3, "Neutral": 2, "Sad": 1}
	mood_numeric = [mood_levels[mood] for mood in moods]

	plt.figure(figsize=(8, 5))
	plt.plot(dates, mood_numeric, marker="o", linestyle="-", color="blue")
	plt.title("Mood Trends Over Time")
	plt.xlabel("Date")
	plt.ylabel("Mood Level")
	plt.yticks([1, 2, 3], ["Sad", "Neutral", "Happy"])
	plt.grid(True)
	plt.show()

# GUI Application
def main_app():
	def submit_mood():
		mood = mood_var.get()
		note = note_entry.get("1.0", tk.END).strip()
		date = datetime.now().strftime("%Y-%m-%d")

		if mood:
			save_mood(date, mood, note)
			messagebox.showinfo("Success", "Mood entry saved successfully!")
			mood_var.set("")
			note_entry.delete("1.0", tk.END)
		else:
			messagebox.showwarning("Input Error", "Please select a mood before submitting.")

	# Setting up the main window
	root = tk.Tk()
	root.title("Daily Mood Tracker")

	# Mood selection
	tk.Label(root, text="How are you feeling today?", font=("Arial", 14)).pack(pady=10)
	mood_var = tk.StringVar()
	tk.Radiobutton(root, text="Happy", variable=mood_var, value="Happy").pack(anchor=tk.W)
	tk.Radiobutton(root, text="Neutral", variable=mood_var, value="Neutral").pack(anchor=tk.W)
	tk.Radiobutton(root, text="Sad", variable=mood_var, value="Sad").pack(anchor=tk.W)

	# Note entry
	tk.Label(root, text="Add a note (optional):", font=("Arial", 12)).pack(pady=10)
	note_entry = tk.Text(root, width=40, height=5)
	note_entry.pack()

	# Buttons
	tk.Button(root, text="Submit", command=submit_mood, bg="lightblue", width=15).pack(pady=10)
	tk.Button(root, text="View Mood Trends", command=plot_mood_trends, bg="lightgreen", width=15).pack(pady=5)

	root.mainloop()

if __name__ == "__main__":
	setup_database()
	main_app()
