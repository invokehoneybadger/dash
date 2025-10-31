from flask import Flask, render_template, jsonify
import threading, requests, time

app = Flask(__name__)

# 👁 Define your swarm
EYES = {
    1: "192.168.10.1",
    2: "192.168.10.2",
    3: "192.168.10.3",
    4: "192.168.10.4",
    5: "192.168.10.5",
    6: "192.168.10.6",
    7: "192.168.10.7",
    8: "192.168.10.8"
}

# 🧠 Runtime state
swarm_data = {
    eye_id: {
        "ip": ip,
        "connected": False,
        "rssi": None,
        "heap": None,
        "psram": None,
        "temp": None,
        "uptime": None,
        "motion": False,
        "last_seen": 0
    } for eye_id, ip in EYES.items()
}

# 🌐 Polling logic
def poll_eye(eye_id, ip):
    url = f"http://{ip}/status"
    try:
        res = requests.get(url, timeout=1.5)
        if res.status_code == 200:
            data = res.json()
            swarm_data[eye_id].update({
                "connected": True,
                "rssi": data.get("wifi_rssi"),
                "heap": data.get("heap_free"),
                "psram": data.get("psram_free"),
                "temp": data.get("temperature"),
                "uptime": data.get("uptime"),
                "motion": data.get("motion", False),
                "last_seen": time.time()
            })
        else:
            swarm_data[eye_id]["connected"] = False
    except Exception:
        swarm_data[eye_id]["connected"] = False

def swarm_poll_loop():
    while True:
        threads = []
        for eye_id, ip in EYES.items():
            t = threading.Thread(target=poll_eye, args=(eye_id, ip))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        time.sleep(2)  # every 2 seconds

# 🧩 API endpoints
@app.route("/")
def index():
    return render_template("index.html", swarm=swarm_data)

@app.route("/api/status")
def api_status():
    return jsonify(swarm_data)

# 🚀 Start background thread
threading.Thread(target=swarm_poll_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
