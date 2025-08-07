from flask import Flask, request, jsonify
from executor import run_in_jail

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run_script():
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400

    result = run_in_jail(code)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")