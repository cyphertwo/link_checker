from flask import Flask, request, jsonify
import asyncio
from batch_check import batch_verify  

app = Flask(__name__)

@app.route("/verify", methods=["POST"])
def verify():
    """
    Endpoint pour vérifier une liste de posts/links.
    Attends un JSON au format :
    {
        "data": [
            {"forum_url": "...", "target_url": "...", "keyword": "..."},
            ...
        ]
    }
    """
    req_data = request.get_json()
    if not req_data or "data" not in req_data:
        return jsonify({"error": "Données manquantes"}), 400

    data_list = req_data["data"]

    # Exécuter batch async
    results = asyncio.run(batch_verify(data_list))

    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
