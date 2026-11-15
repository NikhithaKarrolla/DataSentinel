
# DataSentinel 🛡️
### AI-Powered Data Quality Intelligence & Anomaly Detection

DataSentinel is an intelligent data quality monitoring platform that helps users upload datasets, analyze data quality, identify anomalies, and generate meaningful insights using AI and Machine Learning.

The platform aims to simplify data validation and make datasets more reliable through automated profiling, quality assessment, and anomaly detection.

## 🚀 Features

- **Dataset Upload:** Upload CSV, Excel (XLSX), and JSON files.
- **Data Profiling:** Analyze rows, columns, missing values, and duplicate records.
- **Data Quality Assessment:** Evaluate dataset quality using automated checks.
- **Anomaly Detection:** Identify unusual data patterns using Machine Learning.
- **AI-Powered Insights:** Generate meaningful explanations and recommendations.
- **Interactive Dashboard:** Visualize dataset statistics and quality metrics.

## 🛠️ Tech Stack

### Frontend
- React.js
- JavaScript
- HTML5
- CSS3

### Backend
- Python
- FastAPI

### Data Processing & Machine Learning
- Pandas
- NumPy
- Scikit-learn
- Isolation Forest

### Database & Visualization
- PostgreSQL
- Plotly

### AI & Deployment
- Gemini API
- Docker
- Git & GitHub

## 🏗️ Project Architecture

```text
DataSentinel/
│
├── frontend/
│   └── React application
│
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── venv/
│
├── README.md
└── .gitignore
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/DataSentinel.git
cd DataSentinel
```

### 2. Backend Setup

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Start the Backend Server

```bash
uvicorn app.main:app --reload
```

Backend runs at:

http://127.0.0.1:8000

API Documentation:

http://127.0.0.1:8000/docs

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome endpoint |
| GET | `/health` | Check API health |
| POST | `/datasets/upload` | Upload and profile dataset |
| POST | `/datasets/quality` | Assess dataset quality |

## 📊 Current Development Status

- [x] Backend setup using FastAPI
- [x] Dataset upload functionality
- [x] Dataset profiling
- [x] Initial data quality assessment
- [ ] Machine Learning anomaly detection
- [ ] React dashboard integration
- [ ] AI-powered insights
- [ ] Database integration
- [ ] Docker deployment

## 🎯 Project Objective

The main objective of DataSentinel is to transform raw datasets into reliable, high-quality data by combining automated data profiling, quality assessment, machine learning, and AI-powered insights.

## 👩‍💻 Author

**Nikhitha Karrolla**

GitHub: https://github.com/NikhithaKarrolla

---

⭐ If you find this project interesting, consider giving it a star!
