# Whitmore Groups — Business Plan Web App

A Flask-powered interactive business plan website.

---

## Preview

![Dashboard Preview](screenshots/dashboard.png)

---

## Features

- Interactive business dashboard
- Tab-based navigation
- Execution checklist with saved progress
- Flask backend API
- JSON-based data storage

---

## Setup (one time)

Make sure Python 3.8+ is installed, then run:

```bash
cd whitmore_app
pip install -r requirements.txt
```

---

## Run

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

---

## What works

| Feature | How it works |
|---|---|
| Tab navigation | Client-side JS + server logs tab visits |
| Execution checklist | Clicks saved to `data/checklist.json` — persists across restarts |
| Progress bar | Live % pulled from `/api/checklist/stats` |
| Reset button | Clears all saved checklist state |

---

## API Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/` | Main business plan page |
| GET | `/api/checklist` | Get all saved checklist states |
| POST | `/api/checklist` | Save a single item `{"id": "task_1", "done": true}` |
| POST | `/api/checklist/reset` | Reset all items |
| GET | `/api/checklist/stats` | Get completion stats |
| GET | `/api/tab/<name>` | Log tab navigation |

---

## File Structure

```
whitmore_app/
├── app.py                  # Flask backend
├── requirements.txt        # Dependencies
├── README.md               # This file
├── data/
│   └── checklist.json      # Auto-created on first use
└── templates/
    └── index.html          # Business plan frontend
```

---

## Contact
Uzair — Whitmore Groups
Whitmoreagency228@gmail.com | +91 90320 25790
