from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def setup_database():
	connection = sqlite3.connect("./mood_tracker.db")
	cursor = connection.cursor()
	cursor.execute("""
		CREATE TABLE IF NOT EXISTS "mood_logs" (
		"id"	INTEGER,
		"date"	TEXT NOT NULL,
		"moodLevel"	INTEGER NOT NULL,
		"moodValue"	TEXT NOT NULL,
		"note"	TEXT,
		PRIMARY KEY("id" AUTOINCREMENT)
	)""")
	connection.commit()
	connection.close()

# Save mood entry to database
def save_mood(date, moodLevel, moodValue, note):
	connection = sqlite3.connect("mood_tracker.db")
	cursor = connection.cursor()
	cursor.execute("INSERT INTO mood_logs (date, moodLevel, moodValue, note) VALUES (?, ?, ?, ?)", (date, moodLevel, moodValue, note))
	connection.commit()
	connection.close()

# Fetch mood data for visualization
def fetch_mood_data(date=None):
	connection = sqlite3.connect("mood_tracker.db")
	cursor = connection.cursor()
	if date:
		date += "%"
		#print("Query:", "SELECT date, moodLevel, moodValue, note FROM mood_logs WHERE date LIKE \"?%\"", (date))
		print(date)
		cursor.execute("SELECT date, moodLevel, moodValue, note FROM mood_logs WHERE date LIKE ?", (date,))
	else:
		cursor.execute("SELECT date, moodLevel, moodValue, note FROM mood_logs")
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
	moodLevel = int(request.form.get('moodLevel'))
	moodValue = request.form.get('moodValue')
	note = request.form.get('note', '')
	date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	if (moodValue) and (moodLevel > 0 and moodLevel < 12):
		save_mood(date, moodLevel, moodValue, note)
		return jsonify({"message": "Mood entry saved successfully!"}), 200
	else:
		return jsonify({"message": "Invalid mood value or mood level."}), 400

@app.route('/mood_data', methods=['GET'])
def mood_data():
	if (request.args.get("date")):
		data = fetch_mood_data(request.args.get("date"))
	else:
		data = fetch_mood_data()
	#mood_levels = {"Happy": 3, "Neutral": 2, "Sad": 1}
	formatted_data = [{"date": row[0], "moodLevel": row[1], "moodValue": row[2], "note": row[3]} for row in data]
	return jsonify(formatted_data)

if __name__ == "__main__":
	setup_database()
	app.run(debug=True)
