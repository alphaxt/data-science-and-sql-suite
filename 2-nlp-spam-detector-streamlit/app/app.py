import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer

import os

# force download
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')



# 1. Set page configuration (Must be the very first Streamlit command)
st.set_page_config(
    page_title="Email/SMS Spam Detector",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for modern styling (Fixed parameter to unsafe_allow_html)
st.markdown("""
    <style>
    /* Main app background and typography */
    .main {
        background-color: #f8f9fa;
    }
    h1 {
        color: #1e3a8a;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #4b5563;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    /* Style the text area container */
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    /* Focus styling for text area */
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3) !important;
    }
    /* Center and style the Predict button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        padding: 0.6rem 2.5rem;
        border-radius: 50px;
        border: none;
        width: 100%;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-1px);
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.3);
    }
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #9ca3af;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)

ps = PorterStemmer()

# 3. Preprocessing functions
def transform_lower_case(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
            
    text = y[:]
    y.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()
    
    for i in text:
        y.append(ps.stem(i))
        
    return " ".join(y)

# 4. Load the model and vectorizer with resource caching (Cloud-Safe Update)
@st.cache_resource
def load_models():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    vectorizer_path = os.path.join(BASE_DIR, 'vectorizer.pkl')
    model_path = os.path.join(BASE_DIR, 'model.pkl')
    
    if not os.path.exists(vectorizer_path):
        CLOUD_DIR = "DataScience-Task4-EmailSpamDetection/app"
        vectorizer_path = os.path.join(CLOUD_DIR, 'vectorizer.pkl')
        model_path = os.path.join(CLOUD_DIR, 'model.pkl')
    
    # Load the verified file paths
    tfidf = pickle.load(open(vectorizer_path, 'rb'))
    model = pickle.load(open(model_path, 'rb'))
    return tfidf, model

try:
    tfidf, model = load_models()
except FileNotFoundError:
    st.error("Model files ('vectorizer.pkl' or 'model.pkl') not found. Please ensure they are in the same folder as app.py.")

# --- UI Header Section ---
st.markdown("<h1>🛡️ AI Intelligent Spam Guard</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Analyze text messages or emails for malicious content instantly using Machine Learning.</p>", unsafe_allow_html=True)

# --- UI Body Card ---
with st.container(border=True):
    st.subheader("Analyze Content")
    input_sms = st.text_area(
        label="Paste your text below:", 
        placeholder="Type or paste the email contents here...",
        height=180,
        label_visibility="collapsed",
        key='email_text'
    )
    
    # Grid columns to align layout/button width cleanly
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_btn = st.button('Verify Content')

# --- Prediction & Display Logic ---
if predict_btn:
    if input_sms.strip() == "":
        st.warning("⚠️ Please enter some text before clicking verify.")
    else:
        with st.spinner('Analyzing patterns...'):
            # 1. Transform the input text
            transformed_sms = transform_lower_case(input_sms)

            # 2. Vectorize the input
            vectorized_sms = tfidf.transform([transformed_sms])

            # 3. Predict output class
            result = model.predict(vectorized_sms)[0]

        # 4. Interactive Display UI of results
        st.write("---")
        st.subheader("Analysis Verdict")
        
        if result == 1:
            st.error("🚨 **Spam Detected!** This text matches known structural patterns of phishing, scam, or unsolicited spam messaging.")
        else:
            st.success("✅ **Safe / Legitimate!** This text appears safe and displays the characteristics of regular human communication.")

# --- Footer ---
st.markdown("<div class='footer'>Secure App Workspace | Built with Streamlit & Scikit-Learn</div>", unsafe_allow_html=True)