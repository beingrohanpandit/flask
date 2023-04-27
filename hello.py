from flask import Flask, render_template,flash,request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#create a Flask Instance

app = Flask(__name__)

# Add DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/user'


app.config['SECRET_KEY'] = "1245"

# Initialize the DataBase

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100),nullable=True, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    # Create a String
    def __repr__(self):
        return'<Name %r>' % self.name

# Create all tables in the database
def create_tables():
    with app.app_context():
        db.create_all()

create_tables()
# Create a Form Class

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


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

# Create a From Page
@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first() 
        if user is None:
            user = Users(name=form.name.data,email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("Data Submitted Successfully")
    user = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
    form=form,
    name=name,
    user=user)


# Create a Update Form
@app.route('/user/update/<int:id>', methods=['GET','POST'])
def update_user(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("Updated Successfull")
            return render_template("update_user.html",
            form = form,
            name_to_update = name_to_update)
        except:
            flash("Please Try Again....")
            return render_template("update_user.html",
            form = form,
            name_to_update = name_to_update)
    else:
        return render_template("update_user.html",
            form = form,
            name_to_update = name_to_update)