#!/bin/bash -l

# Make sure file exists 
if [[ ! -f ${1} ]]; then 
  echo "IP file rule does not exists"
  exit
fi

IP=${1%.*}
ID=$(awk '$2=="id" {id=$4} /Rule id is/{sub("\\.","",$NF); id=$NF} END{print id}' $1)
REGION=${2:-east}

if [[ $2 == "west" ]]; then 
  source SNIC_2020_20-57-west-openrc.sh < <(echo $OS_PASSWORD)
else
  source SNIC_2020_20-57-east-openrc.sh < <(echo $OS_PASSWORD)
fi 

#echo $IP, $ID, $REGION
openstack security group rule delete $ID  && rm ${1}
