from flask import Flask
import socket

app = Flask(__name__)

def get_host_name():
    return socket.gethostname()

def get_host_ip_addr(hostname):
    return socket.gethostbyname(hostname)

@app.route('/')
def home():
    hostname = get_host_name()
    ip_addr = get_host_ip_addr(hostname)
    return f'Hostname: {hostname}.<br/>IP Address: {ip_addr}'

app.run()