from flask import Flask, request, redirect, send_from_directory
import requests
import uuid
from datetime import datetime
import re
from user_agents import parse

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
    brand = ua.device.brand or ""
    model = ua.device.model or ""
    device_name = f"{brand} {model}".strip()

    # Stronger regex for Indian phones
    if not device_name or "Generic" in device_name:
        patterns = [
            r'(Redmi|Xiaomi|Poco)[\s-]?([A-Za-z0-9]+)',
            r'(Realme|Oppo|Vivo)[\s-]?([A-Za-z0-9]+)',
            r'(Samsung)[\s-]?([A-Za-z0-9]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, ua_string, re.I)
            if match:
                device_name = f"{match.group(1)} {match.group(2)}"
                break

    if not device_name:
        device_name = "Unknown Device"

    message = f"""🔥 NEW CLICK - POSSIBLE SCAMMER

🆔 Link ID: {link_id}
⏰ Time: {timestamp}
🌐 IP: {ip}
📱 Device: {device_name}
   OS: {ua.os.family}
   Browser: {ua.browser.family}
🔗 Referrer: {referrer or 'Direct'}"""

    try:
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        )
    except:
        pass

    # Show photo instead of redirect
    return send_from_directory('static', 'photo.jpg')

@app.route('/generate')
def generate():
    link_id = str(uuid.uuid4())[:12]
    full_link = f"https://web-production-39eb45.up.railway.app/track/{link_id}"
    return f"✅ New Tracking Link:\n\n{full_link}"

# Create folder and photo (we'll handle this)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
