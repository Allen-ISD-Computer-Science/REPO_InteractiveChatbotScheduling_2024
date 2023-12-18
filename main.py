from flask import Flask, render_template
import os
app = Flask(__name__)

print(__name__)
"""
@app.route('/')
def hello():
    return 'Hello, World!'
"""
@app.route("/")
def landing():
  return render_template("home.html")

if __name__ == '__main__':
    print("About to run...")
    port = int(os.environ.get('VAPOR_LOCAL_PORT', 5000)) 
    host = os.environ.get('VAPOR_LOCAL_HOST', "127.0.0.1")
    print("About to run with port ", port, " and host ", host)
    app.run(port=port, host=host)

    

    
    
