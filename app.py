import streamlit as st
from PIL import Image
import random
import time
from eda.eda_analysis import display_eda_dashboard
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import firebase_admin
# from firebase_admin import credentials, firestore, storage
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from generate_report import render_report_form
from eda.eda_analysis import display_eda_dashboard
# from firebase_config import initialize_firebase


# Set Streamlit page config
st.set_page_config(page_title="Fruit Quality Predictor", layout="wide")

# initialize_firebase()

# Dummy user database (replace with secure auth later)
user_db = {
    "admin": "password123",
    "loukya": "capstone2025"
}

# Session state for login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login logic
def login(username, password):
    if username in user_db and user_db[username] == password:
        st.session_state.authenticated = True
        st.session_state.username = username
    else:
        st.error("❌ Invalid username or password")

# Logout logic
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None

# Display login page if not authenticated
if not st.session_state.authenticated:
    st.title(" Login to Fruit Quality Predictor")
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    if st.button("Login"):
        login(username, password)
    st.stop()

# Sidebar navigation
menu = st.sidebar.radio(" Navigation", 
    ["🏠 Home", "📊 EDA Dashboard", "📝 Generate Report", "ℹ️ About"])

if menu == "🚪 Logout":
    logout()
    st.success("✅ Logged out successfully!")
    st.experimental_rerun()

# Fun fruit facts
fruit_facts = {
    "unripe": [
        " Unripe fruits are rich in resistant starch, which aids digestion!",
        " Green fruits can help control blood sugar levels.",
    ],
    "ripe": [
        " Ripe fruits are sweeter due to natural sugar development.",
        " Athletes love ripe fruits for their quick energy boost!",
    ],
    "overripe": [
        " Overripe fruits are perfect for baking and smoothies.",
        " They contain higher levels of antioxidants.",
    ],
    "rotten": [
        " Rotten fruits aren't wasted—they enrich compost!",
        " Avoid eating rotten fruits due to harmful bacteria.",
    ],
}

# Simulate GAN transformation
def simulate_gan(stage):
    st.info(f"🎨 Generating {stage.capitalize()} Fruit Image using GANs...")
    time.sleep(2)
    st.success(f"✅ {stage.capitalize()} fruit image generated successfully! (Imagine a cool GAN output here 😉)")

# Home Page
if menu == "🏠 Home":
    st.title("🍎 Welcome to the Fruit Quality Prediction System!")
    st.info(random.choice(sum(fruit_facts.values(), [])))

    # Add workflow visualization
    st.header("🔄 Project Workflow")
    st.write("See how our fruit quality prediction system works:")
    
    # Create workflow steps
    workflow_steps = [
        {"icon": "📷", "title": "Image Capture", "description": "Upload or capture an image of fruits"},
        {"icon": "🔍", "title": "Preprocessing", "description": "Image normalization and enhancement"},
        {"icon": "🧠", "title": "GAN Analysis", "description": "Neural network processes the image"},
        {"icon": "📊", "title": "Classification", "description": "AI determines ripeness category"},
        {"icon": "📱", "title": "Results", "description": "Get quality insights for your produce!"}
    ]

    # Create workflow animation with custom styling
    st.markdown("""
    <style>
    .workflow-container {
        display: flex;
        overflow-x: auto;
        padding: 20px 0;
        margin: 20px 0;
        background: linear-gradient(90deg, rgba(255,245,227,1) 0%, rgba(255,222,89,0.3) 50%, rgba(255,245,227,1) 100%);
        border-radius: 10px;
    }
    .workflow-step {
        min-width: 160px;
        margin: 0 10px;
        padding: 15px;
        text-align: center;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .workflow-step:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    .workflow-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .workflow-title {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .workflow-arrow {
        display: flex;
        align-items: center;
        font-size: 1.5rem;
        color: #FFD700;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    .animated-icon {
        animation: bounce 2s infinite;
        display: inline-block;
    }
    </style>
    
    <div class="workflow-container">
    """, unsafe_allow_html=True)
    
    # Generate workflow steps with arrows between them
    workflow_html = ""
    for i, step in enumerate(workflow_steps):
        workflow_html += f"""
        <div class="workflow-step">
            <div class="workflow-icon animated-icon" style="animation-delay: {i*0.2}s">{step['icon']}</div>
            <div class="workflow-title">{step['title']}</div>
            <div>{step['description']}</div>
        </div>
        """
        
        # Add arrow between steps (except after the last step)
        if i < len(workflow_steps) - 1:
            workflow_html += '<div class="workflow-arrow">➡️</div>'
    
    workflow_html += "</div>"
    st.markdown(workflow_html, unsafe_allow_html=True)
    
    # Interactive demo section
    st.subheader("🔄 See it in action:")
    if st.button("▶️ Start Demo"):
        with st.container():
            for i, step in enumerate(workflow_steps):
                with st.spinner(f"Step {i+1}: {step['title']}"):
                    time.sleep(1)
                st.success(f"✅ {step['title']} completed!")
            st.success("🎉 Process complete! Your fruits have been analyzed.")
    
    # Continue with the rest of your home page...
    st.subheader("🍎 Explore Fruit Ripeness Stages:")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("🍏 Unripe"):
        st.success(random.choice(fruit_facts["unripe"]))
        simulate_gan("unripe")
    if col2.button("🍎 Ripe"):
        st.success(random.choice(fruit_facts["ripe"]))
        simulate_gan("ripe")
    if col3.button("🍯 Overripe"):
        st.success(random.choice(fruit_facts["overripe"]))
        simulate_gan("overripe")
    if col4.button("🟤 Rotten"):
        st.success(random.choice(fruit_facts["rotten"]))
        simulate_gan("rotten")

    st.markdown("### 🍎 Ripeness Journey:")
    ripeness_stages = ["🍏 Unripe", "🍎 Ripe", "🍯 Overripe", "🟤 Rotten"]
    progress_bar = st.progress(0)
    for i, stage in enumerate(ripeness_stages):
        time.sleep(0.5)
        progress_bar.progress((i + 1) * 25)
        st.write(f"🔄 {stage}...")
    st.success("🎉 Fruit ripeness journey complete!")


elif menu == "📊 EDA Dashboard":
    display_eda_dashboard()

# About Page
elif menu == "ℹ️ About":
    st.title("ℹ️ About the Project")
    st.markdown("""
    ## 🍎 Optimized Fruit Quality Prediction System  
    This project uses **Generative Adversarial Networks (GANs)** and **Computer Vision** to predict the ripeness of fruits based on images.

    ### 🔍 Project Goals:
    - Predict fruit ripeness stages accurately.
    - Utilize GANs for data augmentation.
    - Provide an interactive dashboard for EDA.

    ### 🛠️ Tech Stack:
    - **Python**: Core development language.
    - **Streamlit**: Interactive dashboard.
    - **OpenCV & TensorFlow**: Image processing & model training.
    - **GANs**: For synthetic data generation.

    ### 🚀 How it Works:
    1. Upload an image of a fruit.
    2. The system analyzes the image using the trained model.
    3. It predicts the ripeness stage as Unripe, Ripe, Overripe, or Rotten.

    🌿 **"Quality insights for better produce!"**  
    """)
    
if menu == "📝 Generate Report":
    render_report_form()

# Logout handler
# Define the logout function
def logout():
    for key in st.session_state.keys():
        del st.session_state[key]

# In your main navigation/menu code
if st.sidebar.button('Logout'):
    logout()
    st.success("✅ Successfully logged out. See you soon!")
    st.rerun()  # Using st.rerun() instead of st.experimental_rerun()