"""
About Page – Project Information and Documentation.

This page explains the purpose of the project, the technology stack,
and how to use the dashboard.
"""

import streamlit as st

st.set_page_config(page_title="About - Book Scraper", page_icon="ℹ️")

st.title("ℹ️ About This Project")

st.markdown("""
## 📚 Book Scraper System

This project was developed as **Level 1, Task 1** of the Codveda Technology Data Science Internship.

### 🎯 Objective
Build a web scraping system that:
- Collects data from a target website (`books.toscrape.com`)
- Handles pagination and common scraping challenges
- Stores the data in a structured format (CSV + SQLite)
- Provides an interactive dashboard to view and export results

### 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Scraping Engine | `requests` + `BeautifulSoup` + `tenacity` |
| Concurrency | `ThreadPoolExecutor` |
| Backend API | FastAPI + Uvicorn |
| Frontend Dashboard | Streamlit |
| Database | SQLite |
| Deployment | Docker + Docker Compose |

### ✨ Features

- **Concurrent, polite scraping** – respects `robots.txt`, uses random delays and user‑agent rotation
- **Retry logic** – automatically retries failed requests
- **Background scraping** – trigger scraping without blocking the API
- **Real‑time dashboard** – view, filter, sort, and export scraped books
- **Dockerized** – one‑command deployment

### 📁 Project Structure



scraping_system/
├── backend/ # FastAPI application
├── frontend/ # Streamlit dashboard
├── data/ # SQLite database and CSV exports
├── logs/ # Scraper logs
├── config.yaml # Configuration
└── docker-compose.yml



### 🔗 Links

- **GitHub Repository**: [https://github.com/yourusername/scraping_system](https://github.com/yourusername/scraping_system)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Live Dashboard**: [http://localhost:8501](http://localhost:8501)

### 👨‍💻 Author

**Your Name** – Data Science Intern @ Codveda Technology

[LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)

### 📜 License

MIT – free for personal and educational use.

---

*Built with ❤️ for the Codveda internship program.*
""")

# -----------------------------------------------------------------------------
# Add a fun fact or tip
# -----------------------------------------------------------------------------
st.divider()
st.subheader("💡 Fun Fact")
st.info("The website `books.toscrape.com` was created specifically for practicing web scraping. It has 1000 books across 50 pages – perfect for this task!")