from flask import Flask, render_template, request, redirect, url_for
from ai_test_engine import run_full_audit
import threading
import time

app = Flask(__name__, static_folder="static")
app.config.from_object('config')

# In-memory storage for results
current_results = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-audit', methods=['POST'])
def start_audit():
    url = request.form['url']
    thread = threading.Thread(target=run_audit_task, args=(url,))
    thread.start()
    return redirect(url_for('dashboard', url=url))

@app.route('/dashboard')
def dashboard():
    url = request.args.get('url')
    return render_template('dashboard.html', 
                         results=current_results.get(url, {}),
                         url=url)

def run_audit_task(url):
    current_results[url] = {'status': 'running', 'steps': []}
    try:
        results = run_full_audit(url)
        current_results[url] = {
            'status': 'completed',
            'results': results,
            'timestamp': time.time()
        }
    except Exception as e:
        current_results[url] = {
            'status': 'error',
            'message': str(e)
        }
        
        

if __name__ == '__main__':
    app.run(debug=True)