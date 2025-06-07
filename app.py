from flask import Flask, jsonify
from flask_cors import CORS
import joblib
import json

app = Flask(__name__)
CORS(app)  # Enable CORS


# Load the model and job data
model = joblib.load('job_forecasting_model.pkl')
with open('jobs_data.json', 'r') as f:
    job_data = json.load(f)

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = [job['title'] for job in job_data['jobs'] if job['industry'] == 'IT']
    return jsonify({'jobs': jobs})

@app.route('/api/job/<job_title>', methods=['GET'])
def get_job_details(job_title):
    for job in job_data['jobs']:
        if job['title'].lower() == job_title.lower():
            return jsonify({
                'title': job['title'],
                'education': job['education'],
                'skills': job['skills']
            })
    return jsonify({'error': 'Job not found'}), 404

 

if __name__ == "__main__":
    app.run(debug=False, port=5000)  # Disable debug mode temporarily