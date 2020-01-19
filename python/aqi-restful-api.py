#!flask/bin/python
from flask import Flask, jsonify
app = Flask(__name__)
import json
  
port=8181

@app.route("/")
def hello_world():
  return "Hello, World!  This is the RESTful API server for Air Quality Monitoring.  Try hitting /aqi/v1.0/aqi"

#tasks = [
#    {
#        'id': 1,
#        'title': u'Buy groceries',
#        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#        'done': False
#    },
#    {
#        'id': 2,
#        'title': u'Learn Python',
#        'description': u'Need to find a good Python tutorial on the web',
#        'done': False
#    }
#]



@app.route('/aqi/v1.0/aqi', methods=['GET'])
def get_aqi():
    #Proper way to extract from json file by reading json structure
    with open("/var/www/html/aqi.json", "r") as read_file:
        measurementdata = json.load(read_file)
        measurement = measurementdata[-1]
        #print(measurement)
        #aqipm10 = "PM10: " + str(measurement['pm10'])
        #aqipm25 = "PM2.5: " + str(measurement['pm25'])
        #aqiDateTime = str(measurement['time'])
    return jsonify(measurement)

@app.route('/aqi/v1.0/latest', methods=['GET'])
def get_latest_aqi():
    #Proper way to extract from json file by reading json structure
    with open("/var/www/html/aqi.json", "r") as read_file:
        measurementdata = json.load(read_file)
        measurement = measurementdata[-1]
        #print(measurement)
        #aqipm10 = "PM10: " + str(measurement['pm10'])
        #aqipm25 = "PM2.5: " + str(measurement['pm25'])
        #aqiDateTime = str(measurement['time'])
    return jsonify(measurement)
    
@app.route('/aqi/v1.0/all', methods=['GET'])
def get_all_aqi():
    #Proper way to extract from json file by reading json structure
    with open("/var/www/html/aqi.json", "r") as read_file:
        measurementdata = json.load(read_file)
        #measurement = measurementdata[-1]
        #print(measurement)
        #aqipm10 = "PM10: " + str(measurement['pm10'])
        #aqipm25 = "PM2.5: " + str(measurement['pm25'])
        #aqiDateTime = str(measurement['time'])
    return jsonify(measurementdata)

#@app.route('/todo/api/v1.0/tasks', methods=['GET'])
#def get_tasks():
#    return jsonify({'tasks': tasks})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
