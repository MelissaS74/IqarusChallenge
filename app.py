from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    # Read the JSON file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Get form data from the request
    disaster_type = request.json.get('disaster_type')
    population = int(request.json.get('population'))

    print("Disaster type:", disaster_type)
    print("Population:", population)

    # Find a matching case in the JSON data
    for item in data:
        print("Current item:", item)
        if item['disaster_type'].lower() == disaster_type.lower() and item['population_affected'] >= population:
            # Construct resources including only existing ones
            resources = {
                'Staff': {},
                'Facilities': {},
                'Equipment': {},
                'Transport': {},
                'Other Resources': {}
            }

            # Fill in existing resources
            staff_resources = item['resources']['staff']
            for key, value in staff_resources.items():
                resources['Staff'][key.replace('_', ' ').title()] = value

            medical_facilities = item['resources']['medical_facilities']
            for key, value in medical_facilities.items():
                resources['Facilities'][key.replace('_', ' ').title()] = value

            medical_equipment = item['resources']['medical_equipment']
            for key, value in medical_equipment.items():
                resources['Equipment'][key.replace('_', ' ').title()] = value

            transport_resources = item['resources']['transport']
            for key, value in transport_resources.items():
                resources['Transport'][key.replace('_', ' ').title()] = value

            other_resources = item['resources']['other_resources']
            for key, value in other_resources.items():
                resources['Other Resources'][key.replace('_', ' ').title()] = value

            # Remove keys with None values
            resources = {category: {resource: amount for resource, amount in resources.items() if amount is not None} for category, resources in resources.items()}

            # Convert 'Ppe' to 'PPE'
            resources['Equipment'] = {'PPE': resources['Equipment'].pop('Ppe', None)}

            return jsonify(resources)

    return jsonify({'error': 'No similar cases found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
