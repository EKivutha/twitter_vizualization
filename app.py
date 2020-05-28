from flask import Flask
from flask import render_template, jsonify
from info import data
import pandas as pd
#from stream_code import main
import threading
import csv



class Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    
# create application
app = Flask(__name__)
prev_list = list()


@app.route('/')
def index():
    t = Thread()
    t.start()
    return render_template('index.html')

@app.route('/data')
def stream_data():
    '''
    GeoJSON Format
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [125.6, 10.1]
      },
      "properties": {
        "name": "Dinagat Islands"
      }
    }
    '''
    new_data = []
    for item in data:
        temp_data = {}
        temp_data['geometry'] = {}
        temp_data['properties'] = {}
        temp_data['type'] = 'Feature'
        temp_data['geometry']['type'] = 'Point'
        temp_data['geometry']['coordinates'] = item['coordinates']['coordinates']
        temp_data['properties']['name'] = item['text']
        new_data.append(temp_data)
    global prev_list
    if prev_list == []:
        prev_list = new_data[:]
        return jsonify(new_data)
    else:
        d = []
        for item in new_data:
            if item not in prev_list:
                d.append(item)
        prev_list = new_data[:]
        return jsonify(d)



'''@app.route("/")
def index():
    t = Thread()
    t.start()
    with open('traffic2.csv',encoding="utf8") as csv_file:
        data = pd.read_csv(csv_file, delimiter=',')
        
        
        new_data = []
        first_line = True
        for item in data:
            print(data.item)
            temp_data = {}
            temp_data['geometry'] = {}
            temp_data['properties'] = {}
            temp_data['type'] = 'Feature'
            temp_data['geometry']['type'] = item[4]
            temp_data['geometry']['coordinates'] = item[16]
            temp_data['properties']['name'] = item[15]
            new_data.append(temp_data) 
        global prev_list
        if prev_list == []:
            prev_list = new_data[:]
            return jsonify(new_data)
        else:
            d = []
            for item in new_data:
                if item not in prev_list:
                    d.append(item)
            prev_list = new_data[:]
            return jsonify(d)
    return render_template('index.html')'''
    
    
if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="127.0.0.1")
