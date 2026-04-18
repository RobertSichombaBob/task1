"""
Main Streamlit application entry point.

This file configures the multi‑page app and sets up page metadata.
Pages are automatically discovered from the 'pages/' directory.
"""

import streamlit as st
from frontend.utils.api_client import health_check

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Book Scraper Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Sidebar (common across all pages)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://books.toscrape.com/static/oscar/img/logo.png", width=150)
    st.markdown("## 📚 Book Scraper")
    st.markdown("---")
    st.markdown("### Navigation")
    st.page_link("app.py", label="🏠 Home", icon="🏠")
    st.page_link("pages/view_data.py", label="📖 View Data", icon="📖")
    st.page_link("pages/about.py", label="ℹ️ About", icon="ℹ️")
    st.markdown("---")
    
    # Show backend status
    if health_check():
        st.success("✅ Backend API: Online")
    else:
        st.error("❌ Backend API: Offline")
        st.info("Make sure the FastAPI backend is running on port 8000")

# -----------------------------------------------------------------------------
# Main Content (landing page)
# -----------------------------------------------------------------------------
st.title("📚 Book Scraper Dashboard")
st.markdown("""
Welcome to the **Book Scraper Dashboard** – a complete web scraping system for 
[Books to Scrape](http://books.toscrape.com/).

Use the sidebar to navigate:
- **Home** – Trigger new scrapes and view statistics.
- **View Data** – Browse, filter, and export scraped books.
- **About** – Learn about the project and its architecture.
""")

st.info("💡 Tip: Click 'View Data' after triggering a scrape to see the results.")

# -----------------------------------------------------------------------------
# Quick Stats on Home Page
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Books in DB", "—", help="Navigate to 'View Data' to load count")
with col2:
    st.metric("Last Scrape", "Not started", help="Trigger a scrape from the sidebar")
with col3:
    st.metric("API Status", "Checking...")

# Note: The actual stats are loaded in the 'home.py' page, not here.
# This file is just the main entry; the home page is pages/home.py.