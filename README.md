# Simple Flask Hello World App

A minimal Flask application to test basic functionality.

## Structure
```
voteapp/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── run.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   └── templates/
│       └── index.html
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Run with Docker
```bash
docker-compose up --build
```

Then open: http://localhost:8080

## Run locally
```bash
pip install -r requirements.txt
cd app
python run.py
```

Then open: http://localhost:5000
