import streamlit as st
import time
import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from frontend.utils.api_client import trigger_scrape, fetch_book_count

st.set_page_config(page_title="Home - Book Scraper", page_icon="🏠")
st.title("🏠 Scraping Control Panel")

if "scraping_triggered" not in st.session_state:
    st.session_state.scraping_triggered = False
    st.session_state.scraping_message = ""

col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🚀 Start New Scrape", type="primary"):
        with st.spinner("Starting scraping job..."):
            result = trigger_scrape()
            if "message" in result:
                st.session_state.scraping_triggered = True
                st.session_state.scraping_message = result["message"]
                st.success(result["message"])
            else:
                st.error("Failed to start scrape")

if st.session_state.scraping_triggered:
    st.info(f"📢 {st.session_state.scraping_message}")
    st.caption("Scraping runs in the background. Refresh the page or check 'View Data' after ~30 seconds.")

st.markdown("---")
st.subheader("📊 Database Statistics")
auto_refresh = st.checkbox("Auto‑refresh every 10 seconds", value=False)

def display_stats():
    count = fetch_book_count()
    st.metric("Total Books in Database", count)
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

with st.expander("ℹ️ How to use"):
    st.markdown("""
    1. Click **Start New Scrape** to begin collecting book data from `books.toscrape.com`.
    2. The scraping runs in the background – you can leave this page.
    3. After 30–60 seconds, go to **View Data** to see the results.
    4. You can download the data as CSV from the View Data page.
    """)