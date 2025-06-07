from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image, ImageDraw, ImageFont
import json
import os
import io

app = Flask(__name__)

DB_FILE = "users.json"
TEMPLATE_IMAGE = "static/Event_Ticket.jpeg"

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(DB_FILE, "w") as file:
        json.dump(users, file)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name'].strip().lower()
        users = load_users()
        if name in users:
            return redirect(url_for('ticket', username=name))
        else:
            return redirect(url_for('register'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip().lower()
        users = load_users()
        if name not in users:
            users[name] = {"name": name}
            save_users(users)
        return redirect(url_for('ticket', username=name))
    return render_template('register.html')

@app.route('/ticket/<username>')
def ticket(username):
    name = username.capitalize()

    # Load the base image
    
    print("✅ Looking for:", TEMPLATE_IMAGE)
    print("✅ Found:", os.path.exists(TEMPLATE_IMAGE))


    image = Image.open(TEMPLATE_IMAGE)
    draw = ImageDraw.Draw(image)

    # Load font (you can use another if Arial is not available)
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    # Set position (adjust these based on where "Guest Name" is in your image)
    position = (130, 400)  # 🖊️ Adjust to align with "Guest Name"

    # Set text color
    color = (145, 44, 44)  # Match with maroon/burgundy

    draw.text(position, name, fill=color, font=font)

    # Save to memory buffer
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
