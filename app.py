from flask import Flask, request, redirect, render_template, jsonify
import random
import string
import json
import os

app = Flask(__name__)
DATA_FILE = "urls.json"

# Load existing short links
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        url_map = json.load(f)
else:
    url_map = {}

def generate_alias():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/')
def index():
    return render_template('first.html')  # make sure first.html is in "templates" folder

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    long_url = data.get("url")
    custom_alias = data.get("alias")

    if not long_url:
        return jsonify({'error': 'Missing URL'}), 400

    # Use custom alias or generate one
    alias = custom_alias if custom_alias else generate_alias()

    # Prevent overwriting existing alias
    if alias in url_map and url_map[alias] != long_url:
        return jsonify({'error': 'Alias already taken'}), 409

    url_map[alias] = long_url

    # Save updated links
    with open(DATA_FILE, "w") as f:
        json.dump(url_map, f)

    short_url = request.host_url + alias
    return jsonify({'short_url': short_url})

@app.route('/<alias>')
def redirect_short_url(alias):
    long_url = url_map.get(alias)
    if long_url:
        return redirect(long_url)
    return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True)
