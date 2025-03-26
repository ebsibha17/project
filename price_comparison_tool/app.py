from flask import Flask, render_template, request
from pymongo import MongoClient
from static.barchart import generate_bar_chart
from utils.sathya import scrape_sathya_product
from utils.prov import scrape_poorvika_product
import os
app = Flask(__name__)


client = MongoClient("mongodb+srv://ebsibha017:ebsibha@cluster0.kem67.mongodb.net/")
db = client.price_comparison
collection = db.products


chart_path = "static/barchart.html"


@app.route('/')
def index():
    """Delete the existing bar chart on page reload and render the homepage."""
    if os.path.exists(chart_path):
        os.remove(chart_path)  # Delete the bar chart on reload

    return render_template('index.html', products=[], chart_exists=False)


@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission, scrape products, store data, and generate chart."""
    url1 = request.form['url1']
    url2 = request.form['url2']

    data1 = scrape_sathya_product(url1)
    data2 = scrape_poorvika_product(url2)

    if data1:
        collection.update_one({'url': url1}, {'$set': data1}, upsert=True)
    if data2:
        collection.update_one({'url': url2}, {'$set': data2}, upsert=True)

    products = [data for data in (data1, data2) if data]  

    if products:
        generate_bar_chart(products)
    
    return render_template('index.html', products=products, chart_exists=bool(products))

if __name__ == '__main__':
    app.run(debug=True)