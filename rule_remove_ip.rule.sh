#!/bin/bash -l

IP=${1%.*}
ID=$(awk '$2=="id" {id=$4} /Rule id is/{sub("\\.","",$NF); id=$NF} END{print id}' $1)

if [[ $2 == "west" ]]; then 
  source SNIC_2020_20-57-west-openrc.sh < <(echo $OS_PASSWORD)
else
  source SNIC_2020_20-57-east-openrc.sh < <(echo $OS_PASSWORD)
fi 

#echo $ID
openstack security group rule delete $ID
