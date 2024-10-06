from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import email_validator

#creating a flask instance
app = Flask(__name__)     #this helps flask to find all the files in directory

#create a secret key for form
app.config['SECRET_KEY'] = 'Sawara-WTF?'

#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#initialise db
db = SQLAlchemy(app)

#create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' %self.name
    
with app.app_context():
    db.create_all()

class UserForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your email?', validators=[DataRequired(), Email()])
    submit = SubmitField("Submit")

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
        flash("Form Submitted!")
    return render_template('name.html', name=name, form=form)

@app.route('/user/add', methods=["GET","POST"])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        #filter users based on their email and return the firs one, rather their should not be any duplicated users
        user = Users.query.filter_by(email = form.email.data).first()

        #if there is no user
        if user is None:
            user = Users(name = form.name.data, email = form.email.data)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User added !")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name = name, our_users = our_users)

# Create the database before the first request

#invalid url
@app.errorhandler(404)

def page_not_found(e):
    return render_template('404.html'), 404

#internal server error
@app.errorhandler(500)

def internal_server_error(e):
    return render_template('500.html'), 500
