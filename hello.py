from flask import Flask, render_template

#creating a flask instance
app = Flask(__name__)     #this helps flask to find all the files in directory

#create a route decorator
@app.route('/')

def index():
    return "<h1>Hello, World!<h1>"