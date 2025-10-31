from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head><title>HoneyBadger Swarm Dashboard</title></head>
    <body style='background:#0e0e0e;color:#9ef01a;font-family:monospace;text-align:center;'>
        <h1>🐾 HoneyBadger Swarm Dashboard</h1>
        <p>Status: Online</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8181)
