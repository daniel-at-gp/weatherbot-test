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
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("date")
    r=requests.get('https://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=9812c8a8af116387d12e7a699ad13a96')
    json_object = r.json()

    weather=json_object['list']
    for i in range(0,30):
        weatherDate = weather[i]['dt_txt']
        if date[:10] == weatherDate[:10]:
            condition= weather[i]['weather'][0]['description']
            break

    speech = "The forecast for "+city+ " for "+date+" is "+condition
    return {
    "fulfillmentText": speech,
    "source": "apiai-weather-webhook"
#    "fulfillmentMessages": speech,
    }


                            

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

















