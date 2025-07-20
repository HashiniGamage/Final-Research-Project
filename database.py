# main.py - Main application file
import streamlit as st
from pages import home, industries, about, login, signup
import sqlite3
import hashlib

# Page configuration
st.set_page_config(
    page_title="Career Nexus",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Database setup
def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('career_nexus.db')
    cursor = conn.cursor()
    
    # Users table with username column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Industries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS industries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            growth_rate DECIMAL(5,2),
            avg_salary DECIMAL(10,2),
            job_count INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            industry_id INTEGER,
            description TEXT,
            requirements TEXT,
            salary_min DECIMAL(10,2),
            salary_max DECIMAL(10,2),
            demand_score INTEGER,
            growth_projection DECIMAL(5,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (industry_id) REFERENCES industries(id)
        )
    ''')
    
    # User preferences table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            preferred_industries TEXT,
            career_goals TEXT,
            experience_level VARCHAR(50),
            education_level VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize session state
def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'user_logged_in' not in st.session_state:
        st.session_state.user_logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

# Navigation functions
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Authentication functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    conn = sqlite3.connect('career_nexus.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, password_hash FROM users 
        WHERE username = ? OR email = ?
    ''', (username, username))
    
    result = cursor.fetchone()
    conn.close()
    
    if result and result[2] == hash_password(password):
        return {'id': result[0], 'username': result[1]}
    return None

def create_user(username, email, password, first_name, last_name):
    conn = sqlite3.connect('career_nexus.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, hash_password(password), first_name, last_name))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

# Custom CSS
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600;700;800&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .stApp {
        background-color: #0f172a;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 3rem;
        background-color: #0f172a;
        margin-bottom: 0;
        border-bottom: 1px solid #1e293b;
    }
    
    .logo {
        font-weight: 600;
        font-size: 1.50rem;
        color: white;
        cursor: pointer;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        font-weight: 500;
        align-items: center;
    }
    
    .nav-link {
        color: white;
        text-decoration: none;
        cursor: pointer;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        transition: background-color 0.2s;
    }
    
    .nav-link:hover {
        background-color: #1e293b;
    }
    
    .nav-link.active {
        background-color: #1e293b;
        color: #60a5fa;
    }
    
    .btn-nav {
        background-color: white;
        color: #0f172a;
        border: none;
        padding: 0.5rem 1.2rem;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        margin-left: 1rem;
    }
    
    .btn-nav:hover {
        background-color: #e2e8f0;
    }
    
    .main .block-container {
        padding-top: 0;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    .user-info {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: #60a5fa;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# Navigation component
def render_navigation():
    user_section = ""
    if st.session_state.user_logged_in:
        user_section = f"""
        <div class="user-info">
            Welcome, {st.session_state.username}!
            <span class="nav-link" onclick="logout()">Logout</span>
        </div>
        """
    else:
        user_section = """
        <div>
            <span class="nav-link" onclick="navigateTo('login')">Login</span>
            <button class="btn-nav" onclick="navigateTo('signup')">Sign Up</button>
        </div>
        """
    
    current_page = st.session_state.page
    
    st.markdown(f"""
    <div class="nav-container">
        <div class="logo" onclick="navigateTo('home')">Career Nexus</div>
        <div class="nav-links">
            <span class="nav-link {'active' if current_page == 'home' else ''}" onclick="navigateTo('home')">Home</span>
            <span class="nav-link {'active' if current_page == 'industries' else ''}" onclick="navigateTo('industries')">Industries</span>
            <span class="nav-link {'active' if current_page == 'about' else ''}" onclick="navigateTo('about')">About Us</span>
            {user_section}
        </div>
    </div>
    
    <script>
    function navigateTo(page) {{
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: page
        }}, '*');
    }}
    
    function logout() {{
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: 'logout'
        }}, '*');
    }}
    </script>
    """, unsafe_allow_html=True)

# Main application
def main():
    # Initialize database and session state
    init_database()
    init_session_state()
    load_css()
    
    # Handle navigation clicks
    nav_action = st.query_params.get("nav", None)
    if nav_action:
        if nav_action == "logout":
            st.session_state.user_logged_in = False
            st.session_state.username = None
            st.session_state.user_id = None
            st.session_state.page = 'home'
        else:
            st.session_state.page = nav_action
        st.query_params.clear()
    
    # Render navigation
    render_navigation()
    
    # Route to appropriate page
    if st.session_state.page == 'home':
        home.show()
    elif st.session_state.page == 'industries':
        industries.show()
    elif st.session_state.page == 'about':
        about.show()
    elif st.session_state.page == 'login':
        login.show()
    elif st.session_state.page == 'signup':
        signup.show()
    else:
        home.show()

if __name__ == "__main__":
    main()

# ========================
# pages/home.py
# ========================

def show():
    """Render the home page"""
    st.markdown("""
    <div style="background: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.75)), 
                url('https://www.chieflearningofficer.com/wp-content/uploads/2022/01/AdobeStock_409689522.jpeg');
                background-size: cover; background-position: center; min-height: 600px;
                display: flex; align-items: center; padding: 0 3rem; margin: 0 -1rem;">
        <div>
            <h1 style="font-size: 3rem; font-weight: 800; margin-bottom: 1rem; color: white;">
                Discover Your Future Career Path
            </h1>
            <p style="font-size: 1.125rem; color: #d1d5db; margin-bottom: 2rem; max-width: 600px;">
                Explore trending industries, discover in-demand jobs, and get personalized career guidance to build the skills you need for tomorrow's workforce.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Explore Industries", use_container_width=True):
            st.session_state.page = 'industries'
            st.rerun()
    
    with col2:
        if st.button("🚀 Get Started Free", use_container_width=True):
            st.session_state.page = 'signup'
            st.rerun()
    
    # How it works section
    st.markdown("""
    <div style="padding: 60px 20px; text-align: center; background-color: #1f2937; margin: 40px -1rem 0;">
        <h2 style="font-size: 2.5rem; margin-bottom: 10px; color: white;">How Career Nexus Works</h2>
        <p style="font-size: 1.1rem; color: #cbd5e1; margin-bottom: 50px;">
            Follow these simple steps to discover your ideal career path and build the skills needed for success
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background-color: #1e293b; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: white; margin-bottom: 1rem;">Explore Industries</h3>
            <p style="color: #cbd5e1; font-size: 0.9rem;">
                Browse through various industries and discover emerging sectors with high growth potential.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #1e293b; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: white; margin-bottom: 1rem;">View Job Rankings</h3>
            <p style="color: #cbd5e1; font-size: 0.9rem;">
                See which jobs are most in-demand and projected to grow over the next 2 years.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #1e293b; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🗺️</div>
            <h3 style="color: white; margin-bottom: 1rem;">Get Career Path</h3>
            <p style="color: #cbd5e1; font-size: 0.9rem;">
                Discover the skills, education, and experience needed for your desired career.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background-color: #1e293b; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
            <h3 style="color: white; margin-bottom: 1rem;">Start Your Journey</h3>
            <p style="color: #cbd5e1; font-size: 0.9rem;">
                Begin building the skills and qualifications for your future career success.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ========================
# pages/industries.py
# ========================

def show():
    """Render the industries page"""
    st.title("🏭 Trending Industries")
    st.markdown("Discover the fastest-growing industries with the most promising career opportunities")
    
    # Sample industry data
    industries = [
        {
            "name": "Artificial Intelligence",
            "growth": "+15.2%",
            "jobs": "2.3M",
            "avg_salary": "$95,000",
            "description": "AI and machine learning technologies are transforming every industry.",
            "image": "https://cdn.mos.cms.futurecdn.net/cuJ2nHdA2cLngX4bhsHsye.jpg"
        },
        {
            "name": "Renewable Energy",
            "growth": "+12.8%", 
            "jobs": "1.8M",
            "avg_salary": "$78,000",
            "description": "Clean energy sector with massive growth in solar, wind, and battery tech.",
            "image": "https://t4.ftcdn.net/jpg/07/75/36/27/360_F_775362773_Bd1AoHBw1gWH8u7VLm2ki61ntwvXGFmv.jpg"
        },
        {
            "name": "Healthcare",
            "growth": "+8.5%",
            "jobs": "4.1M", 
            "avg_salary": "$72,000",
            "description": "Healthcare technology and telemedicine are revolutionizing patient care.",
            "image": "https://www.crosscountrysearch.com/image/how%20technology%20is%20shaping%20the%20future%20of%20healthcare%20careers.jpg"
        },
        {
            "name": "Cybersecurity", 
            "growth": "+18.4%",
            "jobs": "1.2M",
            "avg_salary": "$105,000", 
            "description": "Critical need for security professionals as cyber threats increase.",
            "image": "https://senlainc.com/wp-content/webp-express/webp-images/uploads/%D0%9E%D0%B1%D0%BB%D0%BE%D0%B6%D0%BA%D0%B0-2560%D1%851600.jpg.webp"
        }
    ]
    
    # Display industries in a grid
    cols = st.columns(2)
    for i, industry in enumerate(industries):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div style="background-color: #1e293b; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                    <img src="{industry['image']}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 15px;">
                    <h3 style="color: white; margin-bottom: 10px;">{industry['name']}</h3>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
                        <span style="background-color: #10b981; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem;">
                            Growth: {industry['growth']}
                        </span>
                        <span style="background-color: #1d4ed8; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem;">
                            Jobs: {industry['jobs']}
                        </span>
                        <span style="background-color: #9333ea; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem;">
                            Avg Salary: {industry['avg_salary']}
                        </span>
                    </div>
                    <p style="color: #cbd5e1; font-size: 0.9rem; margin-bottom: 15px;">{industry['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Explore {industry['name']}", key=f"explore_{i}"):
                    st.info(f"Detailed view for {industry['name']} would be implemented here!")

# ========================
# pages/about.py  
# ========================

def show():
    """Render the about page"""
    st.title("🎯 About Career Nexus")
    
    st.markdown("""
    <div style="background-color: #1e293b; padding: 30px; border-radius: 12px; margin: 20px 0;">
        <h2 style="color: white; margin-bottom: 20px;">Our Mission</h2>
        <p style="color: #cbd5e1; font-size: 1.1rem; line-height: 1.6;">
            Career Nexus is dedicated to empowering individuals with data-driven career insights and personalized guidance. 
            We believe everyone deserves access to information about emerging industries, in-demand skills, and future job markets.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 25px; border-radius: 12px; height: 200px;">
            <h3 style="color: white; margin-bottom: 15px;">🔮 Future-Focused</h3>
            <p style="color: #cbd5e1;">
                Our AI-powered predictions analyze market trends, industry growth patterns, and technological disruptions 
                to forecast which careers will be most valuable in the coming years.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #1e293b; padding: 25px; border-radius: 12px; height: 200px;">
            <h3 style="color: white; margin-bottom: 15px;">📊 Data-Driven</h3>
            <p style="color: #cbd5e1;">
                Every recommendation is backed by comprehensive labor market data, salary analysis, 
                and real-time job posting trends from thousands of employers worldwide.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #1e293b; padding: 30px; border-radius: 12px; margin: 20px 0;">
        <h2 style="color: white; margin-bottom: 20px;">Contact Us</h2>
        <p style="color: #cbd5e1;">
            Have questions or feedback? We'd love to hear from you!<br>
            📧 Email: info@careernexus.com<br>
            📱 Phone: +1 (555) 123-4567<br>
            🏢 Address: 123 Innovation Drive, Tech City, TC 12345
        </p>
    </div>
    """, unsafe_allow_html=True)

# ========================
# pages/login.py
# ========================

def show():
    """Render the login page"""
    st.title("🔐 Login to Career Nexus")
    
    with st.form("login_form"):
        st.markdown("### Welcome Back!")
        username = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)
        
        if submit:
            if username and password:
                user = verify_user(username, password)
                if user:
                    st.session_state.user_logged_in = True
                    st.session_state.username = user['username']
                    st.session_state.user_id = user['id']
                    st.success(f"Welcome back, {user['username']}!")
                    st.session_state.page = 'home'
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
            else:
                st.error("Please enter both username and password!")
    
    st.markdown("---")
    st.markdown("Don't have an account?")
    if st.button("Create Account", use_container_width=True):
        st.session_state.page = 'signup'
        st.rerun()

# ========================  
# pages/signup.py
# ========================

def show():
    """Render the signup page"""
    st.title("📝 Create Your Account")
    
    with st.form("signup_form"):
        st.markdown("### Join Career Nexus Today!")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")
        
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submit = st.form_submit_button("Create Account", use_container_width=True)
        
        if submit:
            if not all([username, email, password, first_name, last_name]):
                st.error("Please fill in all fields!")
            elif password != confirm_password:
                st.error("Passwords don't match!")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long!")
            else:
                user_id = create_user(username, email, password, first_name, last_name)
                if user_id:
                    st.success("Account created successfully!")
                    st.session_state.user_logged_in = True
                    st.session_state.username = username
                    st.session_state.user_id = user_id
                    st.session_state.page = 'home'
                    st.rerun()
                else:
                    st.error("Username or email already exists!")
    
    st.markdown("---")
    st.markdown("Already have an account?")
    if st.button("Login", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()