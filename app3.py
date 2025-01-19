from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

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
def fetch_mood_data(date=None):
	connection = sqlite3.connect("mood_tracker.db")
	cursor = connection.cursor()
	if date:
		print("Query:", "SELECT date, mood, note FROM mood_logs WHERE date LIKE " + "\"" + date + "%\"")
		cursor.execute("SELECT date, mood, note FROM mood_logs WHERE date LIKE " + "\"" + date + "%\"")
	else:
		cursor.execute("SELECT date, mood, note FROM mood_logs")
	data = cursor.fetchall()
	connection.close()
	return data

@app.route('/')
def index():
	return render_template('index2.html')

@app.route('/display')
def display():
	return render_template('index3.html')

@app.route('/submit', methods=['POST'])
def submit_mood():
	mood = request.form.get('mood')
	note = request.form.get('note', '')
	date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	if mood:
		save_mood(date, mood, note)
		return jsonify({"message": "Mood entry saved successfully!"}), 200
	else:
		return jsonify({"message": "Please select a mood."}), 400

@app.route('/mood_data', methods=['GET'])
def mood_data():
	if (request.args.get("date")):
		data = fetch_mood_data(request.args.get("date"))
	else:
		data = fetch_mood_data()
	mood_levels = {"Happy": 3, "Neutral": 2, "Sad": 1}
	formatted_data = [{"date": row[0], "mood": mood_levels[row[1]], "note": row[2]} for row in data]
	return jsonify(formatted_data)

if __name__ == "__main__":
	setup_database()
	app.run(debug=True)
