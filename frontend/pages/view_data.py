"""
View Data Page – Browse, Filter, and Export Scraped Books.

This page displays the scraped books in a table and allows users to:
    - Filter by title, rating, or price range.
    - Sort by any column.
    - Download the current view as CSV.
"""

import streamlit as st
import pandas as pd
from frontend.utils.api_client import fetch_books, fetch_book_count

st.set_page_config(page_title="View Data - Book Scraper", page_icon="📖")

st.title("📖 Scraped Books")
st.markdown("Browse, filter, and export the books scraped from [Books to Scrape](http://books.toscrape.com/).")

# -----------------------------------------------------------------------------
# Pagination Controls
# -----------------------------------------------------------------------------
# Use session state to remember current page across reruns
if "page" not in st.session_state:
    st.session_state.page = 1

BOOKS_PER_PAGE = 50

# Get total count
total_books = fetch_book_count()
total_pages = max(1, (total_books + BOOKS_PER_PAGE - 1) // BOOKS_PER_PAGE)

# Pagination UI
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if st.button("◀ Previous", disabled=(st.session_state.page <= 1)):
        st.session_state.page -= 1
        st.rerun()
with col2:
    st.markdown(f"Page **{st.session_state.page}** of **{total_pages}**")
with col3:
    if st.button("Next ▶", disabled=(st.session_state.page >= total_pages)):
        st.session_state.page += 1
        st.rerun()

# -----------------------------------------------------------------------------
# Fetch Data for Current Page
# -----------------------------------------------------------------------------
offset = (st.session_state.page - 1) * BOOKS_PER_PAGE
books = fetch_books(limit=BOOKS_PER_PAGE, offset=offset)

if not books:
    st.info("No books found. Click 'Start New Scrape' on the Home page to collect data.")
    st.stop()

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(books)

# -----------------------------------------------------------------------------
# Filters (sidebar or expander)
# -----------------------------------------------------------------------------
with st.expander("🔍 Filter & Sort", expanded=False):
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    with col_filter1:
        title_filter = st.text_input("Title contains", "")
    with col_filter2:
        rating_filter = st.multiselect("Rating", options=["One", "Two", "Three", "Four", "Five"])
    with col_filter3:
        price_min = st.number_input("Min price (£)", min_value=0.0, value=0.0, step=1.0)
        price_max = st.number_input("Max price (£)", min_value=0.0, value=100.0, step=1.0)
    
    sort_by = st.selectbox("Sort by", ["id", "title", "price", "rating"])
    sort_order = st.radio("Sort order", ["Ascending", "Descending"], horizontal=True)

# Apply filters
filtered_df = df.copy()
if title_filter:
    filtered_df = filtered_df[filtered_df["title"].str.contains(title_filter, case=False, na=False)]
if rating_filter:
    filtered_df = filtered_df[filtered_df["rating"].isin(rating_filter)]
filtered_df = filtered_df[(filtered_df["price"] >= price_min) & (filtered_df["price"] <= price_max)]

# Apply sorting
ascending = (sort_order == "Ascending")
filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

# -----------------------------------------------------------------------------
# Display Table
# -----------------------------------------------------------------------------
st.subheader(f"Showing {len(filtered_df)} books (filtered from {len(df)} on this page)")
st.dataframe(
    filtered_df,
    use_container_width=True,
    column_config={
        "id": "ID",
        "title": "Title",
        "price": st.column_config.NumberColumn("Price (£)", format="£%.2f"),
        "rating": "Rating",
        "availability": "Availability",
        "scraped_at": "Scraped At",
    },
    height=500
)

# -----------------------------------------------------------------------------
# Export to CSV
# -----------------------------------------------------------------------------
st.markdown("---")
col_export1, col_export2 = st.columns(2)
with col_export1:
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="scraped_books.csv",
        mime="text/csv",
        use_container_width=True
    )
with col_export2:
    if st.button("🗑️ Clear Filters", use_container_width=True):
        st.rerun()