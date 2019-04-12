from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/ezEndpoint',methods=['POST'])
def ezEndpoint():
    data = request.data
    dataJSON = json.loads(data)
    
app.run(debug=True)