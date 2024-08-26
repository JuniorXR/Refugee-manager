#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

DATA_FILE = 'data.json'


def load_data():
	try:
		# Ensure the file exists before attempting to load it
		if os.path.exists('data.json'):
			with open('data.json', 'r') as f:
				data = json.load(f)
		else:
			data = []
	except json.JSONDecodeError:
		# Handle JSON decode error (e.g., if the file is empty or corrupted)
		data = []
	return data

def save_data(data):
	with open(DATA_FILE, 'w') as f:
		json.dump(data, f, indent=4)

def format_number(number):
	# Assuming number is a string and always has 11 digits (e.g., "018XXXXXXXX")
	if len(number) == 11:
		return f"{number[:3]} {number[3:7]} {number[7:]}"
	else:
		# Return the number as is if it doesn't match the expected pattern
		return number


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/view')
def view_entries():
	data = load_data()
	data.sort(key=lambda x: x['name'])
	return render_template('view.html', data=data, format_number=format_number)


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
	if request.method == 'POST':
		name = request.form['name']
		number = request.form['number']
		family_members = request.form['family_members']

		if not name or not number or not family_members.isdigit():
			flash("Please enter valid data.")
			return redirect(url_for('add_entry'))

		entry = {
			"name": name,
			"number": number,
			"family_members": int(family_members)
		}

		data = load_data()
		data.append(entry)
		save_data(data)

		flash("Entry added successfully!")
		return redirect(url_for('view_entries'))

	return render_template('add.html')  # <- Pointing to the new `add.html` template


if __name__ == '__main__':
	app.run(debug=True)