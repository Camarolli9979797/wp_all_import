from flask import Flask, jsonify
import pandas as pd
import requests
from io import StringIO
import os

app = Flask(__name__)

# Define the CSV URL
CSV_URL = 'https://feed.stockfirmati.com/csv/exportdropclang.csv'

# Function to fetch and transform CSV data
def fetch_and_transform_csv(csv_url):
    try:
        # Download CSV from the specified URL
        response = requests.get(csv_url)
        response.raise_for_status()

        # Read CSV into a DataFrame
        df = pd.read_csv(StringIO(response.text), delimiter=',', quotechar='"', on_bad_lines='skip', dtype=str, encoding='utf-8')

        # Transform the DataFrame as needed (add your transformation logic here)
        transformed_data = df.to_dict(orient='records')

        return transformed_data
    except Exception as e:
        return {"error": str(e)}

# Define the route for the API endpoint
@app.route('/api/transformed-csv', methods=['GET'])
def get_transformed_csv():
    # Fetch and transform CSV data
    transformed_data = fetch_and_transform_csv(CSV_URL)
    return jsonify(transformed_data)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
