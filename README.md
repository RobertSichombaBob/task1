# 📚 Book Scraper System – Codveda Level 1 Task 1

A **production‑ready, deployment‑ready web scraping system** that extracts book data from `books.toscrape.com` (an ethical, practice‑friendly website).  
It features:

- 🚀 **FastAPI backend** – REST API to trigger scraping and retrieve data  
- 📊 **Streamlit frontend** – interactive dashboard to view and export scraped books  
- ⚡ **Concurrent scraping** – polite, rate‑limited, with retries and user‑agent rotation  
- 🗄️ **SQLite storage** – persistent database with simple querying  
- 🐳 **Docker & docker‑compose** – one‑command deployment  
- 📝 **Full logging** – errors and info written to both console and file  

---

## 🧠 Why This Stands Out

- **Exceeds requirements** – not just a script, but a complete microservice system  
- **Production patterns** – background tasks, concurrency, retries, configuration management  
- **Maintainable code** – modular structure with separation of concerns  
- **Deployment ready** – containerised with environment variables  
- **Ethical scraping** – respects `robots.txt`, includes polite delays, identifies itself  

---

## 🛠️ Tech Stack

| Component      | Technology                          |
|----------------|-------------------------------------|
| Scraping       | `requests` + `BeautifulSoup`        |
| Concurrency    | `ThreadPoolExecutor`                |
| Resilience     | `tenacity` (retries)                |
| User‑agent     | `fake-useragent`                    |
| Backend API    | FastAPI + Uvicorn                   |
| Frontend       | Streamlit                           |
| Database       | SQLite                              |
| Deployment     | Docker + Docker Compose             |

---

## 📁 Project Structure
scraping_system/
├── README.md # You are here
├── requirements.txt # Python dependencies
├── docker-compose.yml # Multi‑container orchestration
├── Dockerfile # Build image for both services
├── .env.example # Environment variables template
├── config.yaml # Scraper & database settings
├── backend/ # FastAPI application
│ ├── main.py
│ ├── api/
│ │ ├── routes.py
│ │ └── models.py
│ ├── core/
│ │ ├── config.py
│ │ ├── database.py
│ │ └── scraper_engine.py
│ └── services/
├── frontend/ # Streamlit dashboard
│ ├── app.py
│ └── utils/
├── tests/ # Unit tests (pytest)
├── data/ # SQLite DB and CSV exports
└── logs/ # Scraper logs

text

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ (if running locally)
- Docker & Docker Compose (if using containers)

### Option 1: Run with Docker (Recommended)
```bash
git clone https://github.com/yourusername/scraping_system.git
cd scraping_system
docker-compose up --build
Then open:

API documentation: http://localhost:8000/docs

Streamlit dashboard: http://localhost:8501

Option 2: Run Locally (without Docker)
bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Start backend (terminal 1)
uvicorn backend.main:app --reload --port 8000

# Start frontend (terminal 2)
streamlit run frontend/app.py --server.port 8501
🔧 Configuration
Edit config.yaml to adjust:

scraper.max_pages – how many pages to scrape

scraper.concurrency – number of parallel workers

scraper.request_delay – seconds between requests

database.sqlite_path – where to store the database

Environment variables (.env) override YAML settings (see .env.example).

📡 API Endpoints
Method	Endpoint	Description
GET	/api/v1/books	Paginated list of scraped books
GET	/api/v1/books/count	Total number of books in DB
POST	/api/v1/scrape	Trigger scraping (background task)
🧪 Testing
Run unit tests:

bash
pytest tests/ -v
📄 License
MIT – free for personal and educational use.

👨‍💻 Author
Your Name – LinkedIn – GitHub

🙏 Acknowledgements
Books to Scrape for providing a safe scraping environment

Codveda Technology for the internship opportunity

Video Demo: [Link to your LinkedIn/YouTube video]
Live Dashboard: [Deployment URL if any]
GitHub Repository: https://github.com/yourusername/scraping_system

text

---

## 2. `requirements.txt`

```txt
# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0
streamlit==1.28.1
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3

# Scraping enhancements
fake-useragent==1.4.0
tenacity==8.2.3

# Data & configuration
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
pyyaml==6.0.1
pandas==2.1.3

# Utilities
aiofiles==23.2.1
httpx==0.25.1

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
3. 
