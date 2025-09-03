import os
import redis
from flask import Flask, render_template

app = Flask(__name__)
redis_client = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'),
                           port=os.environ.get('REDIS_PORT', 6379),
                           db=0, decode_responses=True)

@app.route('/')
def hello():
    # Increment the visit counter
    visit_count = redis_client.incr('counter')
    # Get the hostname of the container
    hostname = os.environ.get('HOSTNAME', 'Unknown')
    return render_template('index.html', visit_count=visit_count, hostname=hostname)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
