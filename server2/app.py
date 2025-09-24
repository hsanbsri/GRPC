from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    return jsonify({
        "cpu": cpu,
        "memory": mem,
        "status": "alive"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
