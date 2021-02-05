#!/usr/bin/env python3
import json
import os, time
import subprocess
import shlex

t_expire= 86400 # expire time in seconds
ACTION= False
verbose= False

with open('projects.yaml','r') as f:
    PROJECTS=yaml.load(f, yaml.FullLoader)

print(PROJECTS)

def source_env(project,region):
    cmd_txt=f'env -i bash -c "source {project}-{region}-openrc.sh && env"' ; cmd=shlex.split(cmd_txt)
    if verbose : print(cmd_txt)
    proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in proc.stdout:
        (key, _, value) = line.decode().partition("=")
        os.environ[key] = value.rstrip()
    proc.communicate()        

def del_rule(rule):
    cmd_txt=f'openstack security group rule delete {rule}' ; cmd=shlex.split(cmd_txt)
    if verbose : print(cmd_txt)
    proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(stdout)
    print(stderr)



for iproject in PROJECTS.keys():
    for iregion in PROJECTS[iproject]['regions']:
        rule= PROJECTS[iproject]['rules'][0]
        print(">>>>> "+iproject+" Region:"+iregion+" Rule:"+rule+" "+"="*20)

        source_env(iproject,iregion)
        cmd_txt= f'openstack security group rule list -f json {rule}' ; cmd=shlex.split(cmd_txt)
        if verbose : print(cmd_txt)
        proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        rules= json.loads(stdout.decode())

        for irule in rules:
            port= PROJECTS[iproject]['ports'][0]; portrange= port+":"+port
            if irule['Port Range'] == portrange:
                if verbose : print(irule)
                cmd_txt= f'openstack security group rule show -f json {irule["ID"]}'; cmd=shlex.split(cmd_txt)
                if verbose : print(cmd_txt)
                proc= subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = proc.communicate()
                rule_data= json.loads(stdout.decode())
                
                upd_time= time.strptime(rule_data['updated_at'],"%Y-%m-%dT%H:%M:%SZ")
                upd_epoch= time.mktime(upd_time)
                delta= time.time() - upd_epoch
                if delta > t_expire:
                    print(f'>>>>>>> Region: {iregion}  ID rule: {irule["ID"]} delta {delta}')
                    print(str(irule)+"\n")
                    if ACTION : del_rule(irule["ID"])   # delete if ACTION





