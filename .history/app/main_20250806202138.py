from flask import Flask, request, jsonify
from executor import run_in_jail

app = Flask(__name__)

@app.route("/execute", methods=["POST"])
def execute_script():
    code = request.json.get("script")
    if not code:
        return jsonify({"error": "No script provided"}), 400

    # Optionally: validate "def main()" exists in code
    if "def main" not in code:
        return jsonify({"error": "No main() function found"}), 400

    result = run_in_jail(code)
    if result.get("result") is None:
        return jsonify({"error": "main() did not return a JSON-serializable object"}), 400
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
