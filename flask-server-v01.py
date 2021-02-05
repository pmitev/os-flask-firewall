#!/usr/bin/env python3
from flask import Flask, make_response, request, send_from_directory, abort
from flask_ipban import IpBan
import os, time 
import subprocess
import shlex
import json

ip_ban = IpBan()
app = Flask(__name__)
ip_ban.init_app(app)
# ufw allow 6768/tcp


@app.route("/<project>/<region>/<rule>/<port>/<token>", methods=["GET"])
def get_my_ip(project,region,rule,port,token):
    ipaddr= request.remote_addr
    if check_project_port(project,region,rule,port,token):
        print("OK")
        source_env(project,region)
        #add_rule(ipaddr,project,region,rule,port)
        response= make_response("Your IP address: " + ipaddr + " is wite-listed for 24 hours",200)
    else:
        print("Wrong")
        response= make_response('Wrong', 404)
        abort(404)

    response.mimetype = "text/plain"
    return response

@app.route("/<project>/<region>/<rule>/WhiteListed/<token>", methods=["GET"])
def get_white(project,region,rule,token):
    if check_project(project,region,rule,token):
        cmd_txt= f'openstack security group rule list --ingress {rule}';    cmd=shlex.split(cmd_txt)
        print(cmd_txt)
        proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        print(stderr)
        response = make_response(stdout.decode(), 200)
    else:
        print('Wrong')
        response= make_response('Wrong', 404)
        abort(404)

    response.mimetype = "text/plain"
    return response


# =============================================================================================================


def add_rule(ip, project, region, rule, port):
    T= time.strftime("%Y-%m-%dT%H:%M:%S")

    with open("ip_witelist.dat", 'a') as fo:
        fo.write(str(time.time()) + ip +" "+project+" "+region+" "+rule+" "+port+" "+T+"\n")
    fo.close()

    cmd_txt=f'openstack security group rule create {rule} --protocol tcp --dst-port {port}:{port} --remote-ip {ip}/32';     cmd=shlex.split(cmd_txt)
    print(cmd_txt)
    proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    print(stderr)
    with open(str(ip)+".rule", 'ab') as fo1:
        fo1.write( (">>> "+T+"\n").encode())
        fo1.write( (">>> "+project+" "+region+"\n").encode())
        fo1.write(stdout)
        fo1.write(stderr)
    fo1.close()

def check_project(project,region,rule,token):
    return (project in PROJECTS.keys()) and (region in PROJECTS[project]['regions']) and (rule in PROJECTS[project]['rules']) and (token == PROJECTS[project]['token'])


def check_project_port(project,region,rule,port,token):
    return (project in PROJECTS.keys()) and (region in PROJECTS[project]['regions']) and (rule in PROJECTS[project]['rules']) and (port in PROJECTS[project]['ports']) and (token == PROJECTS[project]['token'])


def source_env(project,region):
    cmd_txt=f'env -i bash -c "source {project}-{region}-openrc.sh && env"' ; cmd=shlex.split(cmd_txt)
    print(cmd_txt)
    proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in proc.stdout:
        (key, _, value) = line.decode().partition("=")
        os.environ[key] = value.rstrip()
    proc.communicate()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    return True

if __name__ == '__main__':

#    PROJECTS={'SNIC_2020_20-57': {'regions': ['east-1', 'C3SE'],
#      'token': '97df913f-6789-4d74-8617-5afad9e5ccc6',
#      'rules': ['Rstudio'],
#      'ports': ['8787'] }
#      }

    with open('projects.json','r') as f:
        PROJECTS=json.load(f)

    app.run(host="0.0.0.0", port=5000, debug=True)
