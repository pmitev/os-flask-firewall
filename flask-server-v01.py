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


@app.route("/<project>/<region>/<rule>/<token>", methods=["GET"])
def get_my_ip(project,region,rule,token):
    #return jsonify({'ip': request.remote_addr}), 200
    ipaddr= request.remote_addr
    text= "Your IP address: " + ipaddr + " is wite-listed for 24 hours"
    if check_project(project,region,rule,token):
        print("OK")
        source_env(project,region,rule,token)
        #add_rule(ipaddr,project,region,rule)
        print(os.environ['OS_REGION_NAME'])
    else:
        print("Wrong")
        text="Wrong"
    return text, 200

@app.route("/<project>/<region>/<rule>/WhiteListed/<token>", methods=["GET"])
def get_white(project,region,rule,token):
    cmd_txt= f'openstack security group rule list --ingress {rule}';    cmd=shlex.split(cmd_txt)
    print(cmd_txt)
    proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    print(stderr)
    response = make_response(stdout.decode(), 200)
    response.mimetype = "text/plain"
    return response



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def add_rule(ip, project, region, rule):
    cmd_txt=f'openstack security group rule create {rule} --protocol tcp --dst-port 8787:8787 --remote-ip {ip}/32';     cmd=shlex.split(cmd_txt)
    print(cmd_txt)
    proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    print(stderr)

def check_project(project,region,rule,token):
    if (project in PROJECTS.keys()) and (region in PROJECTS[project]['regions']) and (rule in PROJECTS[project]['rules']) and (token == PROJECTS[project]['token']):
        return True
    else:
        return False

def source_env(project,region,rule,token):
    cmd_txt=f'env -i bash -c "source {project}-{region}-openrc.sh && env"' ; cmd=shlex.split(cmd_txt)
    print(cmd_txt)
    proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in proc.stdout:
        (key, _, value) = line.decode().partition("=")
        os.environ[key] = value.rstrip()
    proc.communicate()
    return True

if __name__ == '__main__':
    PROJECTS={'SNIC_2020_20-57': {'regions': ['east-1', 'C3SE'],
      'token': '97df913f-6789-4d74-8617-5afad9e5ccc6',
      'rules': ['Rstudio'] }}

    app.run(host="0.0.0.0", port=5000, debug=True)
