# AI Talent Agent 🚀

An AI-powered system that analyzes job descriptions and candidate resumes to rank and match candidates based on skills, semantic similarity, and interest.

---

## 📌 Features

* Parse Job Description (JD)
* Extract Resume Information
* Semantic Matching using AI
* Candidate Ranking System
* Interest Scoring
* FastAPI Backend with REST APIs
* Simple Frontend UI

---

## 🛠️ Tech Stack

* **Backend:** FastAPI, Python
* **Frontend:** HTML, CSS, JavaScript
* **AI/NLP:** Semantic similarity, custom scoring
* **Tools:** Git, GitHub, Render

---

## 📂 Project Structure

```
ai-talent-agent/
│
├── backend/
│   ├── main.py
│   ├── parser.py
│   ├── resume_reader.py
│   ├── semantic_matcher.py
│   ├── interest_agent.py
│   ├── requirements.txt
│
├── frontend/
│   └── index.html
│
└── README.md
```

---

## ⚙️ Setup from Scratch

### 1. Clone Repository

```bash
git clone https://github.com/vittavivek/ai-talent-agent.git
cd ai-talent-agent
```

---

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

---

### 3. Run Backend

```bash
uvicorn main:app --reload
```

👉 API Docs:

```
http://127.0.0.1:8000/docs
```

---

### 4. Frontend

* Open `frontend/index.html` in browser

---

## 🚀 Deployment (Render)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/vittavivek/ai-talent-agent.git
git push -u origin main
```

---

### Step 2: Deploy on Render

* Go to https://render.com
* New → Web Service → Select Repo

**Settings:**

```
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port 10000
```

---

### Step 3: Access App

```
https://your-app-name.onrender.com/docs
```

---

## ⚠️ Important Notes

* Do NOT push `venv/` folder
* Keep `requirements.txt` minimal
* Use `.gitignore` to exclude unnecessary files

---

## 👨‍💻 Author

Vivek Vitta

---

## ⭐ Future Improvements

* Add authentication
* Improve AI matching accuracy
* Deploy frontend separately
* Add database integration

---
