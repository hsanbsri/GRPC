from flask import Flask, jsonify
import multiprocessing
import psutil
import time

app = Flask(__name__)

# ---------------- Beban CPU Berat ----------------
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

# Jalankan 1 process per core
num_cores = multiprocessing.cpu_count()
for _ in range(num_cores):
    p = multiprocessing.Process(target=cpu_worker)
    p.daemon = True
    p.start()

# ---------------- REST API ----------------
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

@app.route('/compute', methods=['GET'])
def compute():
    start = time.time()
    result = heavy_computation()
    end = time.time()
    cpu = psutil.cpu_percent(interval=1)
    return jsonify({
        "cpu": cpu,
        "time_taken": end-start,
        "status": "done",
        "result": result
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
