from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "API Imgur prête 🚀"

@app.route('/extract', methods=['POST'])
def extract_images():
    data = request.json
    url = data.get('url')

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Erreur Imgur"}), 400

    soup = BeautifulSoup(response.text, 'html.parser')

    images = []
    metas = soup.find_all("meta", {"property": "og:image"})
    for meta in metas:
        image_url = meta.get("content")
        if image_url and "i.imgur.com" in image_url:
            images.append(image_url)

    return jsonify({"images": list(set(images))})

# ✅ CE BLOC DOIT ÊTRE PRÉSENT !
if __name__ == '__main__':
    app.run(debug=True)
