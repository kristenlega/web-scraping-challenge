# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# route for index.html
@app.route("/")
def index():
    final_dict = mongo.db.final_dict.find_one()
    return render_template("index.html", final_dict=final_dict)

# route for scrape
@app.route("/scrape")
def scrape():
    final_dict = mongo.db.final_dict
    final_data = scrape_mars.scrape()
    final_dict.update({}, final_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
