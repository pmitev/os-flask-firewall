#!/usr/bin/env python3
from flask import Flask, make_response, request, send_from_directory
from flask import jsonify
from flask_ipban import IpBan
import os 
import subprocess    
import shlex

ip_ban = IpBan()
app = Flask(__name__)
ip_ban.init_app(app)
# ufw allow 6768/tcp


@app.route("/97df913f-6789-4d74-8617-5afad9e5ccc6", methods=["GET"])
def get_my_ip():
    #return jsonify({'ip': request.remote_addr}), 200
    ipaddr= request.remote_addr
    text= "Your IP address: " + ipaddr + " is wite-listed for 24 hours"

    add_rule(ipaddr)
    return text, 200

@app.route("/WhiteListed", methods=["GET"])
def get_white():
    cmd_txt="openstack security group rule list --ingress Rstudio";    cmd=shlex.split(cmd_txt)
    pr= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = pr.communicate()
    print(stderr)
    response = make_response(stdout.decode(), 200)
    response.mimetype = "text/plain"
    return response


def add_rule(ip):
    cmd_txt=f'./add_ip2rule.sh {ip}';     cmd=shlex.split(cmd_txt)
    print(cmd_txt)
    pr= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = pr.communicate()
    print(stderr)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6768, debug=True)
