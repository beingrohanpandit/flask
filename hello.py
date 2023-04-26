from flask import Flask, render_template

#create a Flask Instance

app = Flask(__name__)

#create a route decorator

@app.route('/')
def index():
    name = "Rohan Sharma"
    Fruits = ['Apple', "Banana", "Kiwi", "Orange"]
    return render_template('index.html',name=name,Fruits=Fruits)


# Create a Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

# Internal Server Error
@app.errorhandler(505)
def page_not_found(e):
    return render_template("505.html"),505
