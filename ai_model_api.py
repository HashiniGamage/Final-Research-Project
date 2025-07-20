from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
import re
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global variables to store models and encoders
models = {}
encoders = {}

def load_models():
    """Load all trained models and encoders"""
    try:
        models['rf_model'] = joblib.load('job_forecasting_model.pkl')
        models['kmeans'] = joblib.load('skill_clustering_model.pkl')
        
        encoders['le_job'] = joblib.load('job_encoder.pkl')
        encoders['le_location'] = joblib.load('location_encoder.pkl')
        encoders['le_experience'] = joblib.load('experience_encoder.pkl')
        encoders['mlb'] = joblib.load('skills_binarizer.pkl')
        encoders['le_demand'] = joblib.load('demand_encoder.pkl')
        
        # Load preprocessed data
        models['df_it'] = pd.read_csv('preprocessed_it_jobs.csv')
        
        logger.info("All models and encoders loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        return False

def extract_salary_lower(salary_range):
    """Extract lower bound of salary range"""
    if isinstance(salary_range, str):
        lower = re.match(r'(\d+)', salary_range)
        return int(lower.group(1)) if lower else np.nan
    return np.nan

def recommend_skills(user_skills, top_n=5):
    """Recommend skills based on user's current skills"""
    if not user_skills or not isinstance(user_skills, list):
        return []
    
    try:
        # Transform user skills
        user_skills_vector = encoders['mlb'].transform([user_skills])
        
        # Predict cluster
        cluster = models['kmeans'].predict(user_skills_vector)[0]
        
        # Get jobs in the same cluster
        cluster_jobs = models['df_it'][models['df_it']['Skill_Cluster'] == cluster]
        
        # Get common skills in this cluster
        all_skills = []
        for skills_str in cluster_jobs['Skills_Required']:
            if isinstance(skills_str, str) and skills_str != 'Unknown':
                skills_list = [s.strip() for s in skills_str.split(',')]
                all_skills.extend(skills_list)
        
        # Count skill frequencies
        skill_counts = pd.Series(all_skills).value_counts()
        
        # Filter out skills user already has
        recommended_skills = [skill for skill in skill_counts.index 
                            if skill not in user_skills][:top_n]
        
        return recommended_skills
    except Exception as e:
        logger.error(f"Error recommending skills: {str(e)}")
        return []

def get_industry_predictions(industry, years=2):
    """Get AI predictions for specific industry"""
    try:
        # Sample predictions based on industry
        industry_predictions = {
            "Information Technology": [
                {
                    "job_title": "AI/ML Engineer",
                    "rank": 1,
                    "demand_level": "High",
                    "growth_rate": 85,
                    "description": "Design and develop intelligent algorithms that learn from data and improve over time.",
                    "skills": ["Python", "TensorFlow", "Machine Learning", "Data Analysis", "Neural Networks"],
                    "education": ["Computer Science", "Data Science", "Mathematics", "Statistics"],
                    "salary_range": "LKR 350,000-800,000",
                    "job_outlook": "Excellent"
                },
                {
                    "job_title": "Cybersecurity Analyst",
                    "rank": 2,
                    "demand_level": "High",
                    "growth_rate": 72,
                    "description": "Protect systems and networks from cyber threats by implementing security strategies.",
                    "skills": ["Network Security", "Ethical Hacking", "Risk Assessment", "SIEM Tools"],
                    "education": ["Cybersecurity", "IT", "Computer Science"],
                    "salary_range": "LKR 250,000-600,000",
                    "job_outlook": "Very Good"
                },
                {
                    "job_title": "Cloud Solutions Architect",
                    "rank": 3,
                    "demand_level": "High",
                    "growth_rate": 78,
                    "description": "Design scalable and secure cloud infrastructure using AWS and Azure.",
                    "skills": ["AWS", "Azure", "Cloud Architecture", "DevOps", "Kubernetes"],
                    "education": ["Cloud Computing", "IT", "Software Engineering"],
                    "salary_range": "LKR 400,000-900,000",
                    "job_outlook": "Excellent"
                }
            ],
            "Healthcare & Medical": [
                {
                    "job_title": "Telemedicine Specialist",
                    "rank": 1,
                    "demand_level": "High",
                    "growth_rate": 92,
                    "description": "Provide remote healthcare services using digital technologies.",
                    "skills": ["Digital Health", "Patient Care", "Medical Technology", "Telehealth Platforms"],
                    "education": ["Medicine", "Health Informatics", "Nursing"],
                    "salary_range": "LKR 200,000-500,000",
                    "job_outlook": "Excellent"
                },
                {
                    "job_title": "Healthcare Data Analyst",
                    "rank": 2,
                    "demand_level": "Medium",
                    "growth_rate": 76,
                    "description": "Analyze medical data to improve patient outcomes and operational efficiency.",
                    "skills": ["Healthcare Analytics", "Statistical Analysis", "Medical Coding", "R", "Python"],
                    "education": ["Health Information", "Statistics", "Public Health"],
                    "salary_range": "LKR 180,000-450,000",
                    "job_outlook": "Very Good"
                }
            ],
            "Finance & Banking": [
                {
                    "job_title": "Fintech Developer",
                    "rank": 1,
                    "demand_level": "High",
                    "growth_rate": 81,
                    "description": "Develop financial technology solutions and payment systems.",
                    "skills": ["Blockchain", "Payment Systems", "Financial Modeling", "API Development"],
                    "education": ["Computer Science", "Finance", "Mathematics"],
                    "salary_range": "LKR 300,000-700,000",
                    "job_outlook": "Excellent"
                }
            ]
        }
        
        return industry_predictions.get(industry, [])
    except Exception as e:
        logger.error(f"Error getting industry predictions: {str(e)}")
        return []

# API Routes
@app.route('/predict_demand', methods=['POST'])
def predict_demand():
    """Predict job demand based on input parameters"""
    try:
        data = request.json
        
        # Validate input
        required_fields = ['Job_Title', 'Location', 'Experience_Level', 'Salary_Range']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Prepare features
        features = [[
            encoders['le_job'].transform([data['Job_Title']])[0],
            encoders['le_location'].transform([data['Location']])[0],
            encoders['le_experience'].transform([data['Experience_Level']])[0],
            extract_salary_lower(data['Salary_Range']),
            data.get('Month', 1)
        ]]
        
        # Make prediction
        prediction = models['rf_model'].predict(features)[0]
        demand = encoders['le_demand'].inverse_transform([prediction])[0]
        
        return jsonify({
            'Demand_Level': demand,
            'Prediction_Score': float(prediction),
            'Status': 'Success'
        })
    
    except Exception as e:
        logger.error(f"Error in predict_demand: {str(e)}")
        return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500

@app.route('/recommend_skills', methods=['POST'])
def recommend_skills_endpoint():
    """Recommend skills based on user's current skills"""
    try:
        data = request.json
        
        if 'skills' not in data:
            return jsonify({'error': 'Skills field is required'}), 400
        
        user_skills = data['skills']
        top_n = data.get('top_n', 5)
        
        recommended_skills = recommend_skills(user_skills, top_n)
        
        return jsonify({
            'Recommended_Skills': recommended_skills,
            'User_Skills': user_skills,
            'Status': 'Success'
        })
    
    except Exception as e:
        logger.error(f"Error in recommend_skills: {str(e)}")
        return jsonify({'error': 'Skill recommendation failed', 'details': str(e)}), 500

@app.route('/industry_predictions', methods=['POST'])
def industry_predictions():
    """Get AI predictions for specific industry"""
    try:
        data = request.json
        
        if 'industry' not in data:
            return jsonify({'error': 'Industry field is required'}), 400
        
        industry = data['industry']
        years = data.get('years', 2)
        
        predictions = get_industry_predictions(industry, years)
        
        return jsonify({
            'Industry': industry,
            'Predictions': predictions,
            'Prediction_Years': years,
            'Status': 'Success'
        })
    
    except Exception as e:
        logger.error(f"Error in industry_predictions: {str(e)}")
        return jsonify({'error': 'Industry prediction failed', 'details': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': len(models) > 0,
        'encoders_loaded': len(encoders) > 0
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'CareerNexus AI Model API',
        'version': '1.0.0',
        'endpoints': [
            '/predict_demand',
            '/recommend_skills',
            '/industry_predictions',
            '/health'
        ]
    })

if __name__ == '__main__':
    # Load models on startup
    if load_models():
        logger.info("Starting CareerNexus AI Model API...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        logger.error("Failed to load models. Exiting...")