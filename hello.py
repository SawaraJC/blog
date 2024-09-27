from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#creating a flask instance
app = Flask(__name__)     #this helps flask to find all the files in directory

#create a secret key for form
app.config['SECRET_KEY'] = 'Sawara-WTF?'

class NamerForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField("Submit")

#create a route decorator
@app.route('/')

def index():
    first = 'daishinkan'
    return render_template('index.html', first_name = first)

#users route: http://127.0.0.1:5000/user/Sawara
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)

#forms page
@app.route('/name', methods=["GET","POST"])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('name.html', name=name, form=form)

#create custom error page

#invalid url
@app.errorhandler(404)

def page_not_found(e):
    return render_template('404.html'), 404

#internal server error
@app.errorhandler(500)

def internal_server_error(e):
    return render_template('500.html'), 500
