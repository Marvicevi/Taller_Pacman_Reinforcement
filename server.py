import eventlet
eventlet.monkey_patch()

import os
import sys
import json
import subprocess
import socket
import qrcode
from PIL import Image
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uss_pacman_secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Global flag to stop accepting new connections when talk is over
ACCEPTING_CONNECTIONS = True

# Store active processes
active_processes = {}

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

@app.route('/')
def index():
    if not ACCEPTING_CONNECTIONS:
        return "Disculpa, el taller ha terminado y no se aceptan nuevas conexiones.", 403
    return render_template('index.html')

@app.route('/admin')
def admin():
    # Para la nube (Render), request.host_url obtiene tu URL dinámica
    # ej: https://pacman-taller.onrender.com
    url = request.host_url.rstrip('/')
    return render_template('admin.html', url=url, accepting=ACCEPTING_CONNECTIONS)

@app.route('/admin/stop', methods=['POST'])
def stop_connections():
    global ACCEPTING_CONNECTIONS
    ACCEPTING_CONNECTIONS = False
    return jsonify({"status": "stopped"})

@app.route('/admin/start', methods=['POST'])
def start_connections():
    global ACCEPTING_CONNECTIONS
    ACCEPTING_CONNECTIONS = True
    return jsonify({"status": "started"})

@socketio.on('connect')
def handle_connect():
    if not ACCEPTING_CONNECTIONS:
        return False  # Reject connection

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in active_processes:
        process = active_processes[sid]
        if process.poll() is None:
            process.terminate()
        del active_processes[sid]

import eventlet

def process_output(process, sid):
    # Read stdout line by line
    for line in iter(process.stdout.readline, ''):
        line = line.strip()
        if line.startswith('__WEB_DISPLAY__:'):
            json_str = line[len('__WEB_DISPLAY__:'):]
            try:
                data = json.loads(json_str)
                if data.get('type') == 'waiting_for_retest':
                    socketio.emit('training_complete', {}, to=sid)
                    continue
                socketio.emit('game_update', data, to=sid)
            except json.JSONDecodeError:
                pass
        
        # VERY IMPORTANT: Yield control back to eventlet loop 
        # so WebSockets don't freeze and timeout under heavy IO
        eventlet.sleep(0.001)

    process.stdout.close()
    if process.stdin:
        process.stdin.close()

@socketio.on('retest')
def handle_retest():
    sid = request.sid
    if sid in active_processes:
        p = active_processes[sid]
        if p.poll() is None and p.stdin:
            p.stdin.write("retest\n")
            p.stdin.flush()

@socketio.on('start_training')
def handle_start_training(data):
    sid = request.sid
    layout = data.get('layout', 'smallGrid')
    episodes = int(data.get('episodes', 100))
    alpha = float(data.get('alpha', 0.2))
    epsilon = float(data.get('epsilon', 0.05))

    # The total games will be episodes + 1 (the +1 is the testing game where it plays slowly)
    total_games = episodes + 1
    
    # We pass standard args to pacman.py, and use webDisplay
    # -p QLearningAgent
    # -x <episodes> means first <episodes> are quiet (no display updates)
    # -n <total> means play total games
    # -a alpha=0.2,epsilon=0.05
    # -c (this is tricky because pacman.py by default uses graphicsDisplay. We need to patch readCommand to accept a generic module or just patch it)
    
    # Wait, instead of patching everything, we can just edit pacman.py to import WebDisplay directly?
    # No, we can just run pacman.py and tell it to use WebDisplay via Python path or custom args.
    
    # Wait! the user has a custom QLearningAgent or we use standard? "pacman en reinforcement". 
    # Actually, CS188 pacman doesn't have a -c flag for display. It has:
    # -t (textGraphics) or -q (quietGraphics).
    # It hardcodes graphicsDisplay in runGames. We should modify pacman.py to support a --web flag!
    # I'll modify pacman.py and add a --web flag that sets display to WebDisplay.

    # Command
    cmd = [
        sys.executable, 'pacman.py',
        '-p', 'PacmanQAgent', # CS188 RL agent name is typically PacmanQAgent
        '-x', str(episodes),
        '-n', str(total_games),
        '-l', layout,
        '-a', f"alpha={alpha},epsilon={epsilon}",
        '--web' # Custom flag we will add to pacman.py
    ]
    
    # Kill previous if exists
    if sid in active_processes:
        p = active_processes[sid]
        if p.poll() is None:
            p.terminate()

    # Start subprocess
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1 # Line buffered
    )
    
    active_processes[sid] = process
    
    # Start a background thread to read output
    socketio.start_background_task(process_output, process, sid)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    
    print(f"==================================================")
    print(f" Servidor iniciado para el Taller de Pacman")
    print(f" Listo para Cloud Deploy (Render/Railway/etc)")
    print(f" Escuchando en 0.0.0.0:{port}")
    print(f"==================================================")
    
    # Ensure static and templates dir
    if not os.path.exists('static'):
        os.makedirs('static')
    if not os.path.exists('templates'):
        os.makedirs('templates')
        
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
