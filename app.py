import streamlit as st
import base64

# Page configuration
st.set_page_config(
    page_title="Career Nexus",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match your design
def load_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600;700;800&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
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
    }
    
    .logo {
        font-weight: 600;
        font-size: 1.50rem;
        color: white;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
        font-weight: 500;
        align-items: center;
    }
    
    .nav-links a {
        color: white;
        text-decoration: none;
    }
    
    .nav-links a:hover {
        text-decoration: underline;
    }
    
    .btn-signup {
        background-color: white;
        color: #0f172a;
        border: none;
        padding: 0.5rem 1.2rem;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
    }
    
    .hero {
        background: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.75)), 
                    url("https://www.chieflearningofficer.com/wp-content/uploads/2022/01/AdobeStock_409689522.jpeg");
        background-size: cover;
        background-position: center;
        min-height: 600px;
        display: flex;
        align-items: center;
        padding: 0 3rem;
        margin: 0 -1rem;
    }
    
    .hero-content h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: white;
    }
    
    .hero-content p {
        font-size: 1.125rem;
        color: #d1d5db;
        margin-bottom: 2rem;
        max-width: 600px;
    }
    
    .btn-group {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .btn-primary {
        background-color: white;
        color: #0f172a;
        padding: 12px 24px;
        border-radius: 6px;
        font-weight: 600;
        border: none;
        cursor: pointer;
    }
    
    .btn-outline {
        border: 2px solid white;
        background: transparent;
        color: white;
        padding: 12px 24px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
    }
    
    .section {
        padding: 60px 20px;
        text-align: center;
        background-color: #1f2937;
        margin: 0 -1rem;
    }
    
    .section2 {
        padding: 60px 20px;
        text-align: center;
        background-color: #111827;
        margin: 0 -1rem;
    }
    
    .features-section {
        padding: 60px 20px;
        text-align: center;
        background-color: #1f2937;
        margin: 0 -1rem;
    }
    
    .section h2, .section2 h2, .features-section h2 {
        font-size: 2.5rem;
        margin-bottom: 10px;
        color: white;
    }
    
    .section p, .section2 p, .features-section p {
        font-size: 1.1rem;
        color: #cbd5e1;
        margin-bottom: 50px;
    }
    
    .steps, .card-container, .features-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 30px;
        margin-top: 30px;
    }
    
    .step, .card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 20px;
        width: 260px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .feature-card {
        background-color: #1e293b;
        border-radius: 16px;
        width: 400px;
        text-align: left;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        overflow: hidden;
    }
    
    .icon {
        width: 60px;
        height: 60px;
        background-color: #2c3e50;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto 20px;
        font-size: 24px;
    }
    
    .step-title, .card-title {
        font-weight: bold;
        margin-bottom: 10px;
        font-size: 1.1rem;
        color: white;
    }
    
    .step-text, .card-content {
        font-size: 0.95rem;
        color: #cbd5e1;
        margin-bottom: 10px;
    }
    
    .feature-content {
        padding: 20px;
    }
    
    .feature-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
        font-size: 20px;
    }
    
    .feature-icon.default { background-color: #1d4ed8; }
    .feature-icon.education { background-color: #9333ea; }
    .feature-icon.skills { background-color: #10b981; }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
        color: white;
    }
    
    .feature-description {
        font-size: 0.95rem;
        color: #cbd5e1;
        margin-bottom: 12px;
    }
    
    .feature-list {
        padding-left: 20px;
        font-size: 0.9rem;
        color: #94a3b8;
    }
    
    .feature-list li {
        margin-bottom: 6px;
        list-style: disc;
    }
    
    .section3 {
        text-align: center;
        padding: 65px 20px;
        background-color: #0f172a;
        margin: 0 -1rem;
    }
    
    .section3 h1 {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        color: white;
    }
    
    .section3 p {
        color: #d1d5db;
        margin-bottom: 20px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .footer {
        background-color: #1f2937;
        color: #fff;
        padding: 40px 20px 20px;
        margin: 0 -1rem;
    }
    
    .footer-container {
        display: flex;
        justify-content: space-between;
        gap: 50px;
        max-width: 1200px;
        margin: auto;
        padding: 0 20px;
        flex-wrap: wrap;
    }
    
    .footer-column {
        flex: 1;
        min-width: 250px;
        max-width: 33%;
    }
    
    .footer-column h3 {
        margin-bottom: 15px;
        color: white;
    }
    
    .footer-column p {
        color: #d1d5db;
        line-height: 1.6;
        font-size: 14px;
    }
    
    .footer-column ul {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .footer-column ul li {
        margin-bottom: 10px;
    }
    
    .footer-column ul li a {
        text-decoration: none;
        color: #d1d5db;
    }
    
    .footer-column ul li a:hover {
        text-decoration: underline;
        color: #fff;
    }
    
    .footer-bottom {
        text-align: center;
        color: #9ca3af;
        margin-top: 40px;
        padding-top: 30px;
        border-top: 1px solid #fff;
    }
    
    .main .block-container {
        padding-top: 0;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    .stMarkdown {
        margin-bottom: 0;
    }
    
    .stButton button {
        background-color: white;
        color: #0f172a;
        border: none;
        padding: 0.5rem 1.2rem;
        border-radius: 6px;
        font-weight: 600;
        border: 2px solid white;
    }
    
    .stButton button:hover {
        background-color: #e2e8f0;
        border: 2px solid #e2e8f0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def home_page():
    # Load custom CSS
    load_css()
    
    # Navigation Bar
    st.markdown("""
    <div class="nav-container">
        <div class="logo">Career Nexus</div>
        <div class="nav-links">
            <a href="#" onclick="window.location.reload()">Home</a>
            <a href="#industries">Industries</a>
            <a href="#about">About Us</a>
            <a href="#login">Login</a>
            <button class="btn-signup">Sign Up</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <h1>Discover Your Future Career Path</h1>
            <p>Explore trending industries, discover in-demand jobs, and get personalized career guidance to build the skills you need for tomorrow's workforce.</p>
            <div class="btn-group">
                <button class="btn-primary">Explore Industries →</button>
                <button class="btn-outline">Get Started Free</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # How It Works Section
    st.markdown("""
    <div class="section">
        <h2>How Career Nexus Works</h2>
        <p>Follow these simple steps to discover your ideal career path and build the skills needed for success</p>
        <div class="steps">
            <div class="step">
                <div class="icon">🔍</div>
                <div class="step-title">Explore Industries</div>
                <div class="step-text">Browse through various industries and discover emerging sectors with high growth potential.</div>
            </div>
            <div class="step">
                <div class="icon">📊</div>
                <div class="step-title">View Job Rankings</div>
                <div class="step-text">See which jobs are most in-demand and projected to grow over the next 2 years.</div>
            </div>
            <div class="step">
                <div class="icon">🗺️</div>
                <div class="step-title">Get Career Path</div>
                <div class="step-text">Discover the skills, education, and experience needed for your desired career.</div>
            </div>
            <div class="step">
                <div class="icon">🚀</div>
                <div class="step-title">Start Your Journey</div>
                <div class="step-text">Begin building the skills and qualifications for your future career success.</div>
            </div>
        </div>
        <button class="btn-primary" style="margin-top: 40px;">Continue to Industries →</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Trending Industries Section
    st.markdown("""
    <div class="section2">
        <h2>Trending Industries</h2>
        <p>Discover the fastest-growing industries with the most promising career opportunities</p>
        <div class="card-container">
            <div class="card">
                <img src="https://cdn.mos.cms.futurecdn.net/cuJ2nHdA2cLngX4bhsHsye.jpg" alt="AI" style="width: 100%; height: 160px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div class="card-title">Artificial Intelligence</div>
            </div>
            <div class="card">
                <img src="https://t4.ftcdn.net/jpg/07/75/36/27/360_F_775362773_Bd1AoHBw1gWH8u7VLm2ki61ntwvXGFmv.jpg" alt="Energy" style="width: 100%; height: 160px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div class="card-title">Renewable Energy</div>
            </div>
            <div class="card">
                <img src="https://www.crosscountrysearch.com/image/how%20technology%20is%20shaping%20the%20future%20of%20healthcare%20careers.jpg" alt="Healthcare" style="width: 100%; height: 160px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div class="card-title">Healthcare</div>
            </div>
            <div class="card">
                <img src="https://senlainc.com/wp-content/webp-express/webp-images/uploads/%D0%9E%D0%B1%D0%BB%D0%BE%D0%B6%D0%BA%D0%B0-2560%D1%851600.jpg.webp" alt="Cybersecurity" style="width: 100%; height: 160px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div class="card-title">Cybersecurity</div>
            </div>
            <div class="card">
                <img src="https://www.skillstork.org/blog/wp-content/uploads/2022/11/modern-education-Skillstork-1568x882.jpg" alt="Education" style="width: 100%; height: 160px; object-fit: cover; border-radius: 12px 12px 0 0;">
                <div class="card-title">Education</div>
            </div>
        </div>
        <button class="btn-primary" style="margin-top: 40px;">View All Industries →</button>
    </div>
    """, unsafe_allow_html=True)
    
        
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-container">
            <div class="footer-column">
                <h3>Career Nexus</h3>
                <p>Your trusted partner in career exploration and future planning. Discover trending industries, in-demand jobs, and the skills you need to succeed in tomorrow's workforce.</p>
            </div>
            <div class="footer-column">
                <h3>Quick Links</h3>
                <ul>
                    <li><a href="#">Explore Industries</a></li>
                    <li><a href="#">About Us</a></li>
                    <li><a href="#">Career Guide</a></li>
                </ul>
            </div>
            <div class="footer-column">
                <h3>Support</h3>
                <ul>
                    <li><a href="#">Help Center</a></li>
                    <li><a href="#">Contact Us</a></li>
                    <li><a href="#">Privacy Policy</a></li>
                    <li><a href="#">Terms of Service</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            © 2025 Career Nexus. All rights reserved.
        </div>
    </div>
    """, unsafe_allow_html=True)

def industries_page():
    load_css()
    st.markdown("## Industries Page")
    st.write("This would be your industries page content")
    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        st.rerun()

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Main app logic
if st.session_state.page == 'home':
    home_page()
elif st.session_state.page == 'industries':
    industries_page()

# Navigation JavaScript (optional)
st.markdown("""
<script>
function navigateToIndustries() {
    console.log('Navigate to industries');
}

function navigateToHome() {
    console.log('Navigate to home');
}
</script>
""", unsafe_allow_html=True)