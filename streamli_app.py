import streamlit as st
import requests
import time

# Set page configuration
st.set_page_config(page_title="IT Job Recommender", layout="wide")

# Initialize session state
if 'step' not in st.session_state:
    st.session_state['step'] = 'industry_selection'
if 'jobs' not in st.session_state:
    st.session_state['jobs'] = []
if 'job_details' not in st.session_state:
    st.session_state['job_details'] = None

# Title
st.title("IT Job Recommender")

# Step 1: Industry Selection
if st.session_state['step'] == 'industry_selection':
    st.header("Select IT Industry")
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Explore IT Jobs"):
            try:
                with st.spinner("Fetching jobs..."):
                    st.write("Attempting to connect to Flask backend...")
                    response = requests.get("http://localhost:5000/api/jobs", timeout=5)
                    if response.status_code == 200:
                        st.session_state['jobs'] = response.json()['jobs']
                        st.session_state['step'] = 'job_selection'
                        st.write("Jobs fetched successfully!")
                    else:
                        st.error(f"Error fetching jobs: Status {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend: {str(e)}")
                st.write("Please ensure Flask server is running at http://localhost:5000")

# Step 2: Job Selection
if st.session_state['step'] == 'job_selection':
    st.header("Future-Demanding IT Jobs")
    if st.session_state['jobs']:
        selected_job = st.selectbox("Choose a Job", st.session_state['jobs'])
        if st.button("Get Educational Path & Skills"):
            try:
                with st.spinner("Fetching job details..."):
                    response = requests.get(f"http://localhost:5000/api/job/{selected_job}", timeout=5)
                    if response.status_code == 200:
                        st.session_state['job_details'] = response.json()
                        st.session_state['step'] = 'job_details'
                    else:
                        st.error(f"Error fetching job details: Status {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend: {str(e)}")
                st.write("Please ensure Flask server is running at http://localhost:5000")
    else:
        st.warning("No jobs available. Please go back and try again.")

# Step 3: Display Educational Path and Skills
if st.session_state['step'] == 'job_details' and st.session_state['job_details']:
    job = st.session_state['job_details']
    st.header(f"Recommendations for {job['title']}")
    st.subheader("Educational Pathway")
    st.markdown(f"**{job['education']}**")
    st.subheader("Required Skills")
    for skill in job['skills']:
        st.markdown(f"- {skill}")
    if st.button("Back to Jobs"):
        st.session_state['step'] = 'job_selection'
    if st.button("Start Over"):
        st.session_state['step'] = 'industry_selection'
        st.session_state['job_details'] = None

# Replace this:
response = requests.get("http://localhost:5000/api/jobs")

# With explicit error handling:
try:
    response = requests.get("http://localhost:5000/api/jobs", timeout=2)
    response.raise_for_status()  # Raises HTTPError for bad status codes
    st.session_state['jobs'] = response.json()['jobs']
except requests.exceptions.RequestException as e:
    st.error(f"Backend connection failed: {str(e)}")
    st.session_state['jobs'] = ["Backend offline - using dummy data", "Data Scientist"]  # Fallback

        