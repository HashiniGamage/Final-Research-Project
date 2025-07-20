import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import hashlib
import joblib
import json
from datetime import datetime
import re
import os

# Page configuration
st.set_page_config(
    page_title="Career Nexus",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .industry-card {
        background: linear-gradient(135deg, #1e293b, #334155);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #3b82f6;
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .job-item {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #10b981;
        margin: 0.5rem 0;
    }
    
    .skill-tag {
        background: #3b82f6;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.8rem;
    }
    
    .metric-card {
        background: rgba(59, 130, 246, 0.1);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #3b82f6;
        text-align: center;
    }
    
    .coming-soon-card {
        background: linear-gradient(135deg, #374151, #4b5563);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        border: 2px dashed #6b7280;
    }
    
    .info-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #3b82f6);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .stSelectbox > div > div {
        background: #1e293b;
        border: 1px solid #3b82f6;
        border-radius: 8px;
    }
    
    .footer {
        background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
        color: white;
        padding: 3rem 2rem 1rem 2rem;
        margin-top: 4rem;
        border-radius: 20px 20px 0 0;
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899, #f59e0b);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .footer-content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .footer-section h3 {
        color: #3b82f6;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .footer-section p, .footer-section li {
        color: #cbd5e1;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    
    .footer-section ul {
        list-style: none;
        padding: 0;
    }
    
    .footer-section li:hover {
        color: #3b82f6;
        cursor: pointer;
        transition: color 0.3s ease;
    }
    
    .social-icons {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .social-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        text-decoration: none;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .social-icon:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }
    
    .footer-bottom {
        border-top: 1px solid #475569;
        padding-top: 1.5rem;
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        position: relative;
    }
    
    .footer-bottom::before {

        position: absolute;
        left: 50%;
        top: -10px;
        transform: translateX(-50%);
        background: #1e293b;
        padding: 0 10px;
        font-size: 1.2rem;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
        background: rgba(59, 130, 246, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: bold;
        color: #3b82f6;
        display: block;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: #cbd5e1;
        margin-top: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Mock AI Model Class
class MockAIModel:
    def __init__(self):
        self.industries = {
            "Technology": {
                "description": "Leading innovation in software, AI, and digital transformation",
                "jobs": [
                    {"title": "Software Engineer", "demand": "High", "salary": "$70K-120K", "growth": "+15%", "skills": ["Python", "JavaScript", "React", "SQL"]},
                    {"title": "Data Scientist", "demand": "High", "salary": "$80K-130K", "growth": "+22%", "skills": ["Python", "Machine Learning", "Statistics", "SQL"]},
                    {"title": "DevOps Engineer", "demand": "High", "salary": "$75K-125K", "growth": "+18%", "skills": ["AWS", "Docker", "Kubernetes", "Python"]},
                    {"title": "Product Manager", "demand": "Medium", "salary": "$90K-140K", "growth": "+12%", "skills": ["Strategy", "Analytics", "Communication", "Agile"]},
                    {"title": "UI/UX Designer", "demand": "Medium", "salary": "$60K-100K", "growth": "+13%", "skills": ["Design", "Figma", "User Research", "Prototyping"]}
                ]
            },
            "Healthcare": {
                "description": "Advancing medical care and health technology",
                "jobs": [
                    {"title": "Nurse Practitioner", "demand": "High", "salary": "$60K-90K", "growth": "+28%", "skills": ["Patient Care", "Clinical Skills", "Communication"]},
                    {"title": "Medical Technologist", "demand": "Medium", "salary": "$45K-70K", "growth": "+11%", "skills": ["Laboratory Skills", "Analysis", "Equipment Operation"]}
                ]
            },
            "Finance": {
                "description": "Managing financial services and investment strategies",
                "jobs": [
                    {"title": "Financial Analyst", "demand": "Medium", "salary": "$55K-85K", "growth": "+8%", "skills": ["Excel", "Financial Modeling", "Analysis"]},
                    {"title": "Investment Banker", "demand": "Medium", "salary": "$80K-150K", "growth": "+6%", "skills": ["Finance", "Analysis", "Communication"]}
                ]
            }
        }
        
        self.educational_paths = {
            "Python": ["Online Python Courses", "Computer Science Degree", "Bootcamps"],
            "Machine Learning": ["ML Specialization", "Data Science Masters", "Online Courses"],
            "JavaScript": ["Web Development Bootcamp", "Frontend Development Course", "CS Degree"],
            "AWS": ["AWS Certification", "Cloud Computing Course", "DevOps Training"]
        }
    
    def get_job_details(self, industry, job_title):
        jobs = self.industries.get(industry, {}).get("jobs", [])
        for job in jobs:
            if job["title"] == job_title:
                return {**job, "description": f"Exciting opportunities in {job_title} with competitive salary and growth prospects."}
        return None
    
    def recommend_education(self, skills):
        recommendations = []
        for skill in skills:
            paths = self.educational_paths.get(skill, [f"{skill} Training"])
            recommendations.extend(paths)
        return list(set(recommendations))
    
    def get_skill_recommendations(self, current_skills, job_title):
        for industry_data in self.industries.values():
            for job in industry_data["jobs"]:
                if job["title"] == job_title:
                    required_skills = job["skills"]
                    missing_skills = [skill for skill in required_skills if skill not in current_skills]
                    return missing_skills
        return []

# Database functions
def init_database():
    conn = sqlite3.connect('career_platform.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # User preferences table
    c.execute('''CREATE TABLE IF NOT EXISTS user_preferences
                 (user_id INTEGER,
                  industry TEXT,
                  experience_level TEXT,
                  location TEXT,
                  skills TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password):
    conn = sqlite3.connect('career_platform.db')
    c = conn.cursor()
    try:
        password_hash = hash_password(password)
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                 (username, email, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('career_platform.db')
    c = conn.cursor()
    password_hash = hash_password(password)
    c.execute("SELECT id, username FROM users WHERE username = ? AND password_hash = ?",
             (username, password_hash))
    user = c.fetchone()
    conn.close()
    return user

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_industry' not in st.session_state:
    st.session_state.selected_industry = None

# Initialize database
init_database()

@st.cache_resource
def load_ai_model():
    return MockAIModel()

ai_model = load_ai_model()

def show_navigation():
    # Create a container for the navigation bar
    nav_container = st.container()
    
    with nav_container:
        # Create two columns - left for logo, right for navigation (reversed from before)
        logo_col, nav_col = st.columns([1, 3])
        
        with logo_col:
            # Logo and branding on the left
            st.markdown("""
            <div style="text-align: left; padding: 10px;">
                <h2 style="margin: 0; color: #3b82f6;">🚀 Career Nexus </h2>
                <p style="margin: 0; font-style: italic; color: #6b7280; font-size: 14px;">IT Industry Focus</p>
            </div>
            """, unsafe_allow_html=True)
            
        with nav_col:
            # Navigation buttons
            if st.session_state.user is None:
                nav_pages = [
                    ("🏠 Home", "home"),
                    ("💼 Industries", "industries"),
                    ("📝 Sign Up", "signup"),
                    ("🔐 Login", "login"),
                ]
            else:
                nav_pages = [
                    ("🏠 Home", "home"),
                    ("💼 Industries", "industries"),
                    ("🚪 Logout", "logout"),
                ]
        
            # Create columns for navigation buttons
            nav_button_cols = st.columns(len(nav_pages))
            for idx, (label, page_key) in enumerate(nav_pages):
                with nav_button_cols[idx]:
                    if st.button(label, key=f"nav_{page_key}_main", use_container_width=True):
                        if page_key == "logout":
                            st.session_state.user = None
                            st.session_state.page = "home"
                            st.session_state.selected_industry = None
                            st.session_state.selected_job = None
                        else:
                            st.session_state.page = page_key
                            if page_key in ["home", "industries"]:  # Removed profile from this list
                                st.session_state.selected_industry = None
                                st.session_state.selected_job = None
                        st.rerun()
    
    # Add a separator line
    st.markdown("""
    <hr style="margin: 20px 0; border: none; height: 2px; background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899, #f59e0b); border-radius: 2px;">
    """, unsafe_allow_html=True)

# Main Content Pages
def home_page():
    # Hero section
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### Transform Your Career Journey with AI
        
        Our advanced AI model analyzes market trends, skill demands, and career paths for your professional growth.
        """)
        
          
    
    # Features grid
    st.markdown("### ✨ Key Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="industry-card">
            <h4>📊 Demand Forecasting</h4>
            <p>AI-powered predictions on job market trends and career opportunities for the next 2 years.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="industry-card">
            <h4>🎯 Skill Recommendations</h4>
            <p>Skill gap analysis based on career.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="industry-card">
            <h4>🎓 Education Pathways</h4>
            <p>Educational routes including degrees, certifications, and online courses.</p>
        </div>
        """, unsafe_allow_html=True)

def industries_page():
    if st.session_state.user is None:
        st.warning("🔒 Please login to explore demanding jobs and get personalized recommendations!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔐 Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
        with col2:
            if st.button("📝 Sign Up", use_container_width=True):
                st.session_state.page = 'signup'
                st.rerun()
        return

    st.title("💼 Industry Analysis")
    st.markdown("Enter your details to get AI-powered job predictions")
    
    # Input form
    with st.form("industry_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            industry = st.selectbox(
                "Select Industry",
                ["Technology", "Healthcare", "Finance", "Manufacturing", "Education", "Retail"]
            )
        
        with col2:
            location = st.text_input("Enter Location (City, State/Country)")
        
        submit_button = st.form_submit_button("🔍 Analyze Jobs", type="primary")
        
        if submit_button:
            if industry and location:
                if industry in ai_model.industries:
                    display_results(industry, location)
                else:
                    st.markdown("""
                    <div class="coming-soon-card">
                        <h2>🚧 Coming Soon!</h2>
                        <p>Analysis for <strong>{}</strong> industry is coming soon!</p>
                        <p>We're working hard to bring you comprehensive insights for this industry.</p>
                        <p><em>Expected launch: Q3 2025</em></p>
                    </div>
                    """.format(industry), unsafe_allow_html=True)
            else:
                st.error("Please fill in all fields")

def display_results(industry, location):
    """Display analysis results"""
    st.markdown("---")
    st.success(f"✅ Analysis complete for {industry} industry in {location}")
    
    industry_data = ai_model.industries[industry]
    jobs = industry_data["jobs"]
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Jobs Found", len(jobs))
    with col2:
        high_demand_jobs = [job for job in jobs if job["demand"] == "High"]
        st.metric("High Demand Jobs", len(high_demand_jobs))
    with col3:
        avg_growth = sum([int(job["growth"].replace("+", "").replace("%", "")) for job in jobs]) / len(jobs)
        st.metric("Avg Growth Rate", f"+{avg_growth:.0f}%")
    
    # Results sections
    tab1, tab2, tab3 = st.tabs(["🎯 Demanding Jobs", "🛠️ Skills Needed", "🎓 Education Pathways"])
    
    with tab1:
        st.markdown("### Top Demanding Jobs")
        for i, job in enumerate(jobs, 1):
            demand_color = "🔴" if job["demand"] == "High" else "🟡"
            st.markdown(f"""
            <div class="job-item">
                <h4>{demand_color} {i}. {job['title']}</h4>
                <p><strong>Demand:</strong> {job['demand']} | <strong>Salary:</strong> {job['salary']} | <strong>Growth:</strong> {job['growth']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Create a simple chart
        job_data = pd.DataFrame(jobs)
        demand_scores = {"High": 95, "Medium": 70, "Low": 40}
        job_data['Demand Score'] = job_data['demand'].map(demand_scores)
        
        fig = px.bar(job_data, x='Demand Score', y='title', orientation='h',
                    title='Job Demand Scores', color='Demand Score',
                    color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Essential Skills in Demand")
        
        # Collect all skills and their job associations
        skill_job_map = {}
        for job in jobs:
            for skill in job["skills"]:
                if skill not in skill_job_map:
                    skill_job_map[skill] = []
                skill_job_map[skill].append(job["title"])
        
        # Sort skills by frequency
        sorted_skills = sorted(skill_job_map.items(), key=lambda x: len(x[1]), reverse=True)
        
        # Display skills with associated jobs
        for skill, related_jobs in sorted_skills:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e293b, #334155);
                      padding: 1rem;
                      border-radius: 10px;
                      border: 1px solid #3b82f6;
                      margin: 0.5rem 0;
                      color: white;'>
                <h4 style='margin:0;color:#3b82f6;'>🔹 {skill}</h4>
                <p style='margin:5px 0;color:#94a3b8;'>Required in {len(related_jobs)} jobs:</p>
                <p style='margin:0;font-size:0.9em;color:#64748b;'>{', '.join(related_jobs)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Create skills frequency chart
        skill_freq = {skill: len(jobs) for skill, jobs in skill_job_map.items()}
        fig_skills = px.bar(
            x=list(skill_freq.values()),
            y=list(skill_freq.keys()),
            orientation='h',
            title='Most In-Demand Skills',
            labels={'x': 'Number of Jobs', 'y': 'Skill'},
            color=list(skill_freq.values()),
            color_continuous_scale='viridis'
        )
        fig_skills.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_skills, use_container_width=True)
    
    with tab3:
        st.markdown("### 🎓 Recommended Education Pathways")
        # Collect all skills from jobs - FIXED THIS PART
        all_skills = []
        for job in jobs:
            if 'skills' in job:  # Changed from 'Skills_Required' to 'skills'
                all_skills.extend(job['skills'])  # Direct access since it's already a list
        
        unique_skills = list(set(all_skills))
        
        # Define education pathways based on skills
        education_pathways = {
            'Degree Programs': {
                'Python': 'BSc in Computer Science',
                'Java': 'BSc in Software Engineering',
                'Machine Learning': 'BSc in Data Science',
                'SQL': 'BSc in Information Technology',
                'Cloud': 'BSc in Cloud Computing'
            },
            'Professional Certifications': {
                'AWS': 'AWS Certified Solutions Architect',
                'Azure': 'Microsoft Azure Fundamentals',
                'Python': 'Python Professional Certification',
                'Java': 'Oracle Certified Professional',
                'Security': 'CompTIA Security+'
            },
            'Short Courses': {
                'Web Development': 'Full Stack Development Bootcamp',
                'Data Science': 'Data Science Specialization',
                'DevOps': 'DevOps Engineering Course',
                'UI/UX': 'UI/UX Design Bootcamp',
                'Agile': 'Agile Project Management'
            }
        }
        
        # Display recommendations in tabs
        degree_tab, cert_tab, course_tab = st.tabs(['🎯 Degrees', '📜 Certifications', '📚 Short Courses'])
        
        with degree_tab:
            st.markdown("**Recommended Degree Programs:**")
            for skill in unique_skills:
                for key, value in education_pathways['Degree Programs'].items():
                    if key.lower() in skill.lower():
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #1e293b, #334155);
                                  padding: 1.5rem;
                                  border-radius: 15px;
                                  border: 1px solid #3b82f6;
                                  margin: 1rem 0;
                                  color: white;'>
                            <h4 style='margin:0;color:#3b82f6;'>🎓 {value}</h4>
                            <p style='margin:8px 0;color:#94a3b8;'>Related Skill: {skill}</p>
                            <p style='margin:0;font-size:0.9em;color:#64748b;'>⏱️ Duration: 3-4 years</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        with cert_tab:
            st.markdown("**Recommended Professional Certifications:**")
            for skill in unique_skills:
                for key, value in education_pathways['Professional Certifications'].items():
                    if key.lower() in skill.lower():
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #1e293b, #334155);
                                  padding: 1.5rem;
                                  border-radius: 15px;
                                  border: 1px solid #3b82f6;
                                  margin: 1rem 0;
                                  color: white;'>
                            <h4 style='margin:0;color:#3b82f6;'>📜 {value}</h4>
                            <p style='margin:8px 0;color:#94a3b8;'>Related Skill: {skill}</p>
                            <p style='margin:0;font-size:0.9em;color:#64748b;'>⏱️ Duration: 3-6 months</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        with course_tab:
            st.markdown("**Recommended Short Courses:**")
            for skill in unique_skills:
                for key, value in education_pathways['Short Courses'].items():
                    if key.lower() in skill.lower():
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #1e293b, #334155);
                                  padding: 1.5rem;
                                  border-radius: 15px;
                                  border: 1px solid #3b82f6;
                                  margin: 1rem 0;
                                  color: white;'>
                            <h4 style='margin:0;color:#3b82f6;'>📚 {value}</h4>
                            <p style='margin:8px 0;color:#94a3b8;'>Related Skill: {skill}</p>
                            <p style='margin:0;font-size:0.9em;color:#64748b;'>⏱️ Duration: 2-4 months</p>
                        </div>
                        """, unsafe_allow_html=True)

def signup_page():
    st.title("📝 Create Your Account")
    
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", placeholder="Enter your username")
            email = st.text_input("Email", placeholder="your.email@example.com")
        
        with col2:
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        submitted = st.form_submit_button("🚀 Create Account", type="primary")
        
        if submitted:
            if not all([username, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                if create_user(username, email, password):
                    st.success("Account created successfully! Please login.")
                    st.balloons()
                    st.session_state.page = 'login'
                    st.rerun()
                else:
                    st.error("Username or email already exists")
    
    st.markdown("---")
    if st.button("Already have an account? Login"):
        st.session_state.page = 'login'
        st.rerun()

def login_page():
    st.title("🔐 Welcome Back")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        submitted = st.form_submit_button("🚀 Login", type="primary")
        
        if submitted:
            if username and password:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success(f"Welcome back, {user[1]}!")
                    st.session_state.page = 'home'
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password")
    
    st.markdown("---")
    if st.button("Don't have an account? Sign up"):
        st.session_state.page = 'signup'
        st.rerun()

def show_footer():
    """Display creative footer on every page"""
    st.markdown("""
    <div class="footer">        
        
    
            © 2025 Career Nexus. All rights reserved. 
        
    </div>
    """, unsafe_allow_html=True)

def main():
    show_navigation()

    # Route to appropriate page
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "industries":
        industries_page()
    elif st.session_state.page == "signup":
        signup_page()
    elif st.session_state.page == "login":
        login_page()
    
    # Always show footer at the bottom
    show_footer()

if __name__ == "__main__":
    main()