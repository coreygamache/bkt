from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get("https://classic.warcraftlogs.com/v1/reports/guild/Released/Pagle/US?api_key=82e9648595b617cdc3806a8868249a8a")
    statuscode = response.status_code
    print(statuscode)
    return 'hello'
