from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

# Helper function to read the CSV and format data correctly
def load_travel_data():
    places = []
    try:
        with open('world_famous_places_2024.csv', mode='r', encoding='utf-8') as file:
            # DictReader automatically turns each row into a dictionary using column headers as keys
            csv_reader = csv.DictReader(file)
            
            # We loop through each row to clean up and convert data types
            for index, row in enumerate(csv_reader):
                formatted_place = {
                    "id": index + 1,  # Adding a unique ID for easier frontend rendering
                    "name": row["Place_Name"],
                    "country": row["Country"],
                    "city": row["City"],
                    "annual_visitors_millions": float(row["Annual_Visitors_Millions"]),
                    "type": row["Type"],
                    "unesco_world_heritage": row["UNESCO_World_Heritage"],
                    "year_built": row["Year_Built"],
                    "entry_fee_usd": int(row["Entry_Fee_USD"]),
                    "best_visit_month": row["Best_Visit_Month"],
                    "region": row["Region"],
                    "tourism_revenue_million_usd": int(row["Tourism_Revenue_Million_USD"]),
                    "average_visit_duration_hours": float(row["Average_Visit_Duration_Hours"]),
                    "famous_for": row["Famous_For"]
                }
                places.append(formatted_place)
    except FileNotFoundError:
        print("Error: world_famous_places_2024.csv file not found!")
    return places

# --- API ENDPOINTS ---

# 1. Endpoint to get all 30 places (with optional filtering by country or region)
@app.route('/api/places', methods=['GET'])
def get_all_places():
    all_places = load_travel_data()
    
    # Optional search filters (e.g., /api/places?country=France)
    country_query = request.args.get('country')
    region_query = request.args.get('region')
    
    if country_query:
        all_places = [p for p in all_places if p['country'].lower() == country_query.lower()]
    if region_query:
        all_places = [p for p in all_places if p['region'].lower() == region_query.lower()]
        
    return jsonify(all_places)

# 2. Endpoint to get a single specific place using its ID
@app.route('/api/places/<int:place_id>', methods=['GET'])
def get_place_by_id(place_id):
    all_places = load_travel_data()
    
    # Search for the place matching the provided ID
    place = next((p for p in all_places if p['id'] == place_id), None)
    
    if place:
        return jsonify(place)
    else:
        return jsonify({"error": f"Place with ID {place_id} not found"}), 404

# Run the backend local server
if __name__ == '__main__':
    # debug=True allows the server to auto-reload whenever you make code changes
    app.run(debug=True, port=5000)