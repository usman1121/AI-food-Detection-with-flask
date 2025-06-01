# 🍔 Food Type Detection App

An AI-powered web application that uses a webcam to detect different food types in real-time. Built with a Flask backend and a machine learning model, this app allows users to interact with a live camera feed, classify food images, and monitor results via an admin dashboard.

## 🚀 Features

- 📷 Real-Time Webcam Detection – Detects food types instantly using your device's camera.
- 🧠 AI Integration – Powered by gemini api.
- 📊 Admin Dashboard – View detection logs, statistics, and manage system activity.
- 🗃️ Data Storage – Logs each prediction with a timestamp into an SQLite database.

## 🛠️ Tech Stack

- **Backend**: Flask, Flask-WTF, Flask-Login
- **Database**: SQLite3
- **ML Model**: google gemini 
- **Frontend**: HTML5, JavaScript (Webcam access)
- **Others**: Jinja2 Templating, Pillow

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/food-detection-app.git
cd food-detection-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py




