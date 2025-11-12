import os
from flask import Flask
import redis

def create_app():
    app = Flask(__name__)
    
    # Configure Redis
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    app.redis_client = redis.Redis.from_url(redis_url, decode_responses=True)
    
    # Configure question
    app.config['VOTE_QUESTION'] = os.environ.get('VOTE_QUESTION', 'Do you like this app?')
    
    # Initialize vote counters
    with app.app_context():
        if not app.redis_client.exists('votes:yes'):
            app.redis_client.set('votes:yes', 0)
        if not app.redis_client.exists('votes:no'):
            app.redis_client.set('votes:no', 0)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app