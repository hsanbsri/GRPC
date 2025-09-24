from flask import Flask, jsonify
import multiprocessing
import psutil
import time

app = Flask(__name__)

def heavy_computation():
    total = 0
    for i in range(1, 50000000):
        total += i
        total *= 1.0001
        total /= 1.00005
    return total

def cpu_worker():
    while True:
        heavy_computation()

if __name__ == "__main__":
    # Jalankan 1 process per core untuk load tinggi
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=cpu_worker)
        p.daemon = True
        p.start()

    @app.route('/status', methods=['GET'])
    def status():
        cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
        cpu_avg = sum(cpu_per_core) / len(cpu_per_core)
        mem = psutil.virtual_memory().percent
        return jsonify({
            "cpu_avg": cpu_avg,
            "cpu_per_core": cpu_per_core,
            "memory": mem,
            "status": "alive"
        })

    app.run(host="0.0.0.0", port=5000)
