from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load trained ML model
model = joblib.load("priority_model.pkl")
LABELS = ["LOW", "MEDIUM", "HIGH"]

@app.route("/infer", methods=["POST"])
def infer():
    data = request.json
    devices = data["devices"]

    policies = []

    for d in devices:
        features = [[
            d["rssi"],
            d.get("throughput", 3.0),
            d.get("rtt", 60),
            d.get("loss", 1),
            d.get("congestion", 0)
        ]]

        pred = model.predict(features)[0]
        priority = LABELS[pred]

        policies.append({
            "mac": d["mac"],
            "priority": priority
        })

    return jsonify({"policies": policies})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=6000)
