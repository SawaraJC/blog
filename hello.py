from flask import Flask, render_template

#creating a flask instance
app = Flask(__name__)     #this helps flask to find all the files in directory

#create a route decorator
@app.route('/')

def index():
    first = 'daishenku'
    return render_template('index.html', first_name = first)

#users route: http://127.0.0.1:5000/user/Sawara
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)

