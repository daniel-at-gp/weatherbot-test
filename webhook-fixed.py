import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = makeResponse(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    speech = 'https://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=9812c8a8af116387d12e7a699ad13a96'
    return {
    "speech": speech,
    "displayText": speech,
    "source": "apiai-weather-webhook"
    }

    if req.get("result").get("action") != "fetchWeatherForecast":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")
    if city is None:
        return None
    r=requests.get('https://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=9812c8a8af116387d12e7a699ad13a96')

    
    speech = "The forecast for"+city+ "for "+date+" is "+condition
    speech = "damned if I know"
    return {
    "speech": speech,
    "displayText": speech,
    "source": "apiai-weather-webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















