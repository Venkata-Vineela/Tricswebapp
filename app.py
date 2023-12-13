# In web_interface/app.py
from flask import Flask, render_template, jsonify
import sqlite3
import plotly.express as px

app = Flask(__name__)

# Sample function to get organization data from the database
def get_organization_data():
    # Replace this with your actual data retrieval logic
    conn = sqlite3.connect('../data/user_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT organization, COUNT(*) FROM users GROUP BY organization")
    organization_data = dict(cursor.fetchall())
    conn.close()
    return organization_data

def get_address_data():
  conn = sqlite3.connect('../data/user_data.db')
  cursor = conn.execute("SELECT street_address, COUNT(*) FROM users GROUP BY street_address")
  address_data = dict(cursor.fetchall())
  conn.close()
  return address_data

# Sample route to render the HTML page
@app.route('/')
def display_user_data_visualization():
    return render_template('index.html')

# Sample route to get organization chart data
@app.route('/get_organization_chart')
def get_organization_chart():
    organization_data = get_organization_data()

    # Create a pie chart using Plotly Express
    fig = px.pie(
        names=list(organization_data.keys()),
        values=list(organization_data.values()),
        title='Distribution of Users by Organization'
    )

    # Convert the Plotly figure to JSON
    chart_json = fig.to_json()

    return jsonify(chart_json)

@app.route('/get_address_chart')
def get_address_chart():

  address_data = get_address_data()
  
  # Create pie chart for address
  fig = px.pie(
        names=list(address_data.keys()),
        values=list(address_data.values()), 
        title='Distribution of Users by Location'
  )

  return jsonify(fig.to_json())

if __name__ == '__main__':
    app.run(debug=True)
