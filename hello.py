from flask import Flask, render_template,flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
#create a Flask Instance

app = Flask(__name__)
app.config['SECRET_KEY'] = "1245"
# Create a Form Class

class NameForm(FlaskForm):
    name = StringField("What is Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


#create a route decorator
@app.route('/')
def index():
    name = "Rohan Sharma"
    Fruits = ['Apple', "Banana", "Kiwi", "Orange", "Pineapple"]
    return render_template('index.html',name=name,Fruits=Fruits)

@app.route('/about')
def about():
    return render_template('about.html')


# Create a Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

# Internal Server Error
@app.errorhandler(505)
def page_not_found(e):
    return render_template("505.html"),505

# Create a Name Page
@app.route('/name',methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    #Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully")
    return render_template("name.html",
    name=name,
    form=form)