#!/bin/bash -l

IP=${1}
REGION=${2:-east} # default region east

if [[ !  ${1} =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Invalid IP address"
  exit
fi

fIP=${IP}.rule

if [[ $2 == "west" ]]; then 
  source SNIC_2020_20-57-west-openrc.sh < <(echo $OS_PASSWORD)
else
  source SNIC_2020_20-57-east-openrc.sh < <(echo $OS_PASSWORD)
fi 

echo "${IP}  $(date +'%Y-%m-%dT%H:%M:%S')  $(date +%s) ${REGION}" | tee -a ip_witelist.dat
echo ">>> ${REGION} $(date +'%Y-%m-%dT%H:%M:%S')"   | tee -a ${fIP}
openstack security group rule create Rstudio --protocol tcp --dst-port 8787:8787 --remote-ip $IP/32    2>&1 | tee -a ${fIP}
