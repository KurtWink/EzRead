from flask import Flask
app = Flask(__name__)

@app.route('/ezEndpoint',methods=['POST']))
def ezEndpoint():
     if request.method == 'POST':
		
