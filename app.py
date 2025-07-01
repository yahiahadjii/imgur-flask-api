from flask import Flask, request, jsonify
import requests
import os
import re

app = Flask(__name__)

# Mets ici ton vrai Client ID Imgur, ou utilise une variable d'environnement sur Render
IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID", "TON_CLIENT_ID_IMGUR")

@app.route('/')
def home():
    return "API Imgur prête 🚀"

@app.route('/extract', methods=['POST'])
def extract_images():
    data = request.json
    url = data.get('url', '')

    # Détecter l'ID d'album ou de galerie
    album_match = re.search(r'imgur\\.com/(?:a|gallery)/([a-zA-Z0-9]+)', url)
    if album_match:
        album_id = album_match.group(1)
        api_url = f"https://api.imgur.com/3/album/{album_id}/images"
        headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            images = [img['link'] for img in data['data']]
            return jsonify({"images": images})
        else:
            return jsonify({"error": "Erreur API Imgur"}), 400

    # Sinon, gestion d'un lien direct classique
    direct_match = re.search(r'(i\\.imgur\\.com/[a-zA-Z0-9]+\\.(jpg|jpeg|png|gif))', url)
    if direct_match:
        return jsonify({"images": [f"https://{direct_match.group(1)}"]})

    # Sinon, gestion d'un lien imgur.com/xxxxxx
    single_match = re.search(r'imgur\\.com/([a-zA-Z0-9]+)$', url)
    if single_match:
        image_id = single_match.group(1)
        return jsonify({"images": [f"https://i.imgur.com/{image_id}.jpg"]})

    return jsonify({"error": "Aucun lien direct trouvé"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
