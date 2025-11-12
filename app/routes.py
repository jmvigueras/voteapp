from flask import Blueprint, render_template, jsonify, request, current_app
import subprocess
import hashlib
import sqlite3

main = Blueprint('main', __name__)

@main.route('/')
def index():
    question = current_app.config.get('VOTE_QUESTION', 'Do you like this app?')
    return render_template('index.html', question=question)

@main.route('/login')
def login_page():
    return render_template('login.html')

# Catch-all route for any undefined path (excluding /api/* routes)
@main.route('/<path:path>')
def catch_all(path):
    # Only handle non-api routes
    if not path.startswith('api/'):
        question = current_app.config.get('VOTE_QUESTION', 'Do you like this app?')
        return render_template('index.html', question=question)
    # For undefined API routes, return 404
    return jsonify({'error': 'API endpoint not found'}), 404

@main.route('/api/vote', methods=['POST'])
def vote():
    data = request.get_json()
    
    if not data or 'vote' not in data:
        return jsonify({'error': 'Missing vote'}), 400
    
    vote_value = data['vote'].lower()
    
    if vote_value not in ['yes', 'no']:
        return jsonify({'error': 'Invalid vote'}), 400
    
    # Increment vote in Redis
    current_app.redis_client.incr(f'votes:{vote_value}')
    
    return jsonify({'success': True, 'message': 'Vote recorded'})

@main.route('/api/results', methods=['GET'])
def results():
    yes_votes = int(current_app.redis_client.get('votes:yes') or 0)
    no_votes = int(current_app.redis_client.get('votes:no') or 0)
    total = yes_votes + no_votes
    
    yes_percentage = round((yes_votes / total) * 100, 1) if total > 0 else 0
    no_percentage = round((no_votes / total) * 100, 1) if total > 0 else 0
    
    return jsonify({
        'yes': yes_votes,
        'no': no_votes,
        'total': total,
        'yes_percentage': yes_percentage,
        'no_percentage': no_percentage
    })

#CWE-78: OS Command Injection
@main.route('/api/ping')
def ping_host():
    host = request.args.get('host', 'localhost')
    
    # Vulnerable: Command injection
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return result.decode()

#A2: Broken Authentication
@main.route('/api/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        
        # Vulnerable: Weak hashing algorithm without salt
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        # Use path relative to app directory
        import os
        db_path = os.path.join(os.path.dirname(__file__), 'database.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return "Login successful", 200
        return "Login failed", 401
    except Exception as e:
        return f"Error: {str(e)}", 500