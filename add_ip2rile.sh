#!/bin/bash -l

IP=${1%}

if [[ $2 == "west" ]]; then 
  source SNIC_2020_20-57-west-openrc.sh < <(echo $OS_PASSWORD)
else
  source SNIC_2020_20-57-east-openrc.sh < <(echo $OS_PASSWORD)
fi 

openstack security group rule create Rstudio --protocol tcp --dst-port 8787:8787 --remote-ip $IP/32
