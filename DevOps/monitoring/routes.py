from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from functools import wraps
import psutil
import docker
import subprocess

monitor_bp = Blueprint('monitoring', __name__, template_folder='templates')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('monitoring.login'))
        return f(*args, **kwargs)
    return decorated_function

@monitor_bp.route('/monitoring', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['logged_in'] = True
        return redirect(url_for('monitoring.menu'))
    return render_template('login.html')

@monitor_bp.route('/monitoring/menu')
@login_required
def menu():
    return render_template('menu.html')

@monitor_bp.route('/monitoring/machine')
@login_required
def machine():
    return render_template('machine.html')

@monitor_bp.route('/monitoring/containers')
@login_required
def containers():
    return render_template('containers.html')

@monitor_bp.route('/monitoring/machine/metrics')
@login_required
def machine_metrics():
    return jsonify({
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent
    })

@monitor_bp.route('/monitoring/containers/list')
@login_required
def container_list():
    client = docker.from_env()
    containers = []
    
    for container in client.containers.list(all=True):
        stats = container.stats(stream=False)
        containers.append({
            'name': container.name,
            'status': container.status,
            'cpu': calculate_cpu_percent(stats),
            'memory': calculate_memory_usage(stats)
        })
    
    return jsonify({'containers': containers})

@monitor_bp.route('/monitoring/machine/terminal')
@login_required
def launch_htop():
    subprocess.Popen(['x-terminal-emulator', '-e', 'htop'])
    return '', 204

@monitor_bp.route('/monitoring/containers/terminal')
@login_required
def launch_lazydocker():
    subprocess.Popen(['x-terminal-emulator', '-e', 'lazydocker'])
    return '', 204

def calculate_cpu_percent(stats):
    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    return round((cpu_delta / system_delta) * 100, 2)

def calculate_memory_usage(stats):
    return round(stats['memory_stats']['usage'] / (1024 * 1024), 2)  # Convert to MB
