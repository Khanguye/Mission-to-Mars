from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   mars_surfaces = mongo.db.mars_surfaces.find()
   return render_template("index.html", mars=mars,mars_surfaces =mars_surfaces )

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

@app.route("/mars/scrape")
def scrape_mars():
   mars_surfaces = mongo.db.mars_surfaces
   mars_surface_data = scraping.scrape_mars_surfaces()
   print(mars_surface_data)
   #delete previous Mars info items
   mars_surfaces.delete_many({})
   #insert new Mars info items
   ids = mars_surfaces.insert_many(mars_surface_data)
   print(ids)
   return "Scraping Successful!"

if __name__ == "__main__":
   app.run(debug=True)