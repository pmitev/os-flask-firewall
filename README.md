# notes

```
export FLASK_APP=ip.py
flask run --host=0.0.0.0 --port=6768
```


```
# flask + 
python3 -m venv venv/flask_flask_openstack
source venv/flask_openstack/bin/activate
python3 -m pip install -U setuptools pip
python3 -m pip install flask flask-ipban python-openstackclient
```







## OpenStack
```
#https://docs.openstack.org/newton/user-guide/cli-nova-configure-access-security-for-instances.html
openstack security group rule list Rstudio
openstack security group rule create Rstudio --protocol tcp --dst-port 8787:8787 --remote-ip 127.00.000.00/32
openstack security group rule show   490050ba-6576-4186-87b6-22ab5329c5d7
openstack security group rule delete 490050ba-6576-4186-87b6-22ab5329c5d7

nova list-secgroup NONMEM3

```

## Example project structure

```
PROJECTS={'SNIC_2020_20-17': {'regions': ['east-1', 'C3SE'],
  'token': '97df913f-6789-4d74-8617-5afad9e5ccc6-42f359',
  'rules': ['Rstudio'], 
  'ports': ['8787'] }   
  }
```

```
SNIC_2020_20-17:
  ports:
  - '8787'
  regions:
  - east-1
  - C3SE
  rules:
  - Rstudio
  token: 97df913f-6789-4d74-8617-5afad9e5ccc6-42f359
```
