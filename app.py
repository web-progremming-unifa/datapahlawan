from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Path to the JSON file
JSON_FILE = 'heroes.json'

def load_heroes():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_heroes(heroes):
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(heroes, file, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    heroes = load_heroes()
    return render_template('index.html', heroes=heroes)

@app.route('/add_hero', methods=['POST'])
def add_hero():
    heroes = load_heroes()
    new_hero = request.get_json()
    heroes.append(new_hero)
    save_heroes(heroes)
    return jsonify({'status': 'success', 'hero': new_hero})

@app.route('/delete_hero/<int:index>', methods=['DELETE'])
def delete_hero(index):
    heroes = load_heroes()
    if 0 <= index < len(heroes):
        deleted_hero = heroes.pop(index)
        save_heroes(heroes)
        return jsonify({'status': 'success', 'hero': deleted_hero})
    return jsonify({'status': 'error', 'message': 'Invalid index'}), 404

# WSGI handler for Vercel
def application(environ, start_response):
    from io import StringIO
    import sys
    old_stdout = sys.stdout
    sys.stdout = result = StringIO()
    app(environ, start_response)
    sys.stdout = old_stdout
    return [result.getvalue().encode('utf-8')]

if __name__ == '__main__':
    app.run(debug=True)