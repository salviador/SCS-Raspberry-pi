#!/bin/bash

echo SCS Library Setup

sudo apt-get -y install mosquitto
sudo apt-get -y install mosquitto-clients


line=$(grep -rnw '/etc/mosquitto/mosquitto.conf' -e 'listener 1883')
#echo ${#line}
#echo ${line}
if  [[ ! ${#line} -gt 1 ]]
then
    sudo echo -e "listener 1883\n" >> /etc/mosquitto/mosquitto.conf
fi

line=$(grep -rnw '/etc/mosquitto/mosquitto.conf' -e 'listener 9001')
if  [[ ! ${#line} -gt 1 ]]
then
    sudo echo -e "listener 9001\n" >> /etc/mosquitto/mosquitto.conf
fi
line=$(grep -rnw '/etc/mosquitto/mosquitto.conf' -e 'protocol websockets')
if  [[ ! ${#line} -gt 1 ]]
then
    sudo echo -e "protocol websockets\n" >> /etc/mosquitto/mosquitto.conf
fi
line=$(grep -rnw '/etc/mosquitto/mosquitto.conf' -e 'allow_anonymous true')
if  [[ ! ${#line} -gt 1 ]]
then
    sudo echo -e "allow_anonymous true\n" >> /etc/mosquitto/mosquitto.conf
fi
sleep 5
sudo systemctl stop mosquitto
sleep 5
sudo systemctl start mosquitto






start_c='sudo python3 /'${PWD#*/}'/APP/main.py'
line=$(grep -rnw '/etc/rc.local' -e "$start_c")
if  [[ ! ${#line} -gt 1 ]]
then
    #sed -i -e "s|exit 0|$start_c \&\nexit 0|g" "/etc/rc.local"
    sudo python3 setup_rclocal.py
fi

sudo chmod -R 7777 '/'${PWD#*/}
sudo chown -R pi '/'${PWD#*/}
sudo chmod -R 7777 '/etc/rc.local'


sudo python3 setup.py install


echo Fine
