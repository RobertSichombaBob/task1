"""
Home Page – Scraping Control Panel.

This page allows users to:
    - Trigger a new scraping job.
    - View real‑time statistics (book count, last scrape time).
    - Monitor the status of ongoing scraping.
"""

import streamlit as st
import time
from frontend.utils.api_client import trigger_scrape, fetch_book_count

st.set_page_config(page_title="Home - Book Scraper", page_icon="🏠")

st.title("🏠 Scraping Control Panel")

# -----------------------------------------------------------------------------
# State Management
# -----------------------------------------------------------------------------
# Use session state to remember scrape status across reruns
if "scraping_triggered" not in st.session_state:
    st.session_state.scraping_triggered = False
if "scraping_message" not in st.session_state:
    st.session_state.scraping_message = ""

# -----------------------------------------------------------------------------
# Trigger Scrape Button
# -----------------------------------------------------------------------------
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🚀 Start New Scrape", type="primary", use_container_width=True):
        with st.spinner("Starting scraping job..."):
            result = trigger_scrape()
            if "message" in result:
                st.session_state.scraping_triggered = True
                st.session_state.scraping_message = result["message"]
                st.success(result["message"])
            else:
                st.error("Failed to start scraping. Check backend logs.")

# -----------------------------------------------------------------------------
# Show status if scraping was triggered recently
# -----------------------------------------------------------------------------
if st.session_state.scraping_triggered:
    st.info(f"📢 {st.session_state.scraping_message}")
    st.caption("Scraping runs in the background. Refresh the page or check 'View Data' after ~30 seconds.")

# -----------------------------------------------------------------------------
# Statistics Section
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("📊 Database Statistics")

# Auto‑refresh every 10 seconds if user wants
auto_refresh = st.checkbox("Auto‑refresh every 10 seconds", value=False)

def display_stats():
    count = fetch_book_count()
    st.metric("Total Books in Database", count, delta=None)
    if count > 0:
        st.success(f"✅ Database contains {count} books. Go to 'View Data' to explore.")
    else:
        st.info("📭 No books yet. Click 'Start New Scrape' to begin.")

if auto_refresh:
    placeholder = st.empty()
    while True:
        with placeholder.container():
            display_stats()
        time.sleep(10)
        st.rerun()
else:
    display_stats()

# -----------------------------------------------------------------------------
# Help Section
# -----------------------------------------------------------------------------
with st.expander("ℹ️ How to use"):
    st.markdown("""
    1. Click **Start New Scrape** to begin collecting book data from `books.toscrape.com`.
    2. The scraping runs in the background – you can leave this page.
    3. After 30–60 seconds, go to **View Data** to see the results.
    4. You can download the data as CSV from the View Data page.
    """)