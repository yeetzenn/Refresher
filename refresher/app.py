
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class Bypass:
    def __init__(self, cookie: str) -> None:
        self.cookie = cookie

    def start_process(self) -> str:
        self.xcsrf_token = self.get_csrf_token()
        self.rbx_authentication_ticket = self.get_rbx_authentication_ticket()
        return self.get_set_cookie()

    def get_set_cookie(self) -> str:
        response = requests.post(
            "https://auth.roblox.com/v1/authentication-ticket/redeem",
            headers={"rbxauthenticationnegotiation": "1"},
            json={"authenticationTicket": self.rbx_authentication_ticket}
        )
        set_cookie_header = response.headers.get("set-cookie")
        if not set_cookie_header:
            raise ValueError("An error occurred while getting the set-cookie header")
        return set_cookie_header.split(".ROBLOSECURITY=")[1].split(";")[0]

    def get_rbx_authentication_ticket(self) -> str:
        response = requests.post(
            "https://auth.roblox.com/v1/authentication-ticket",
            headers={
                "rbxauthenticationnegotiation": "1",
                "referer": "https://www.roblox.com/camel",
                "Content-Type": "application/json",
                "x-csrf-token": self.xcsrf_token
            },
            cookies={".ROBLOSECURITY": self.cookie}
        )
        ticket = response.headers.get("rbx-authentication-ticket")
        if not ticket:
            raise ValueError("An error occurred while getting the rbx-authentication-ticket")
        return ticket

    def get_csrf_token(self) -> str:
        response = requests.post(
            "https://auth.roblox.com/v2/logout",
            cookies={".ROBLOSECURITY": self.cookie}
        )
        xcsrf_token = response.headers.get("x-csrf-token")
        if not xcsrf_token:
            raise ValueError("Failed to get X-CSRF-TOKEN. Check if your Roblox cookie is valid.")
        return xcsrf_token

@app.route('/')
def home():
    with open('index.html', 'r') as f:
        return f.read()

@app.route('/style.css')
def style():
    with open('style.css', 'r') as f:
        response = app.response_class(
            response=f.read(),
            status=200,
            mimetype='text/css'
        )
        return response

@app.route('/script.js')
def script():
    with open('script.js', 'r') as f:
        response = app.response_class(
            response=f.read(),
            status=200,
            mimetype='application/javascript'
        )
        return response

@app.route('/api/process-cookie', methods=['POST'])
def process_cookie():
    try:
        data = request.get_json()
        cookie = data.get('cookie', '').strip()
        
        if not cookie:
            return jsonify({'error': 'Please provide a .ROBLOSECURITY cookie'}), 400
            
        bypass = Bypass(cookie)
        new_cookie = bypass.start_process()
        
        return jsonify({'success': True, 'cookie': new_cookie})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
