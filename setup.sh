#!/bin/bash
#打开外部端口 5000
sudo iptables -I INPUT -p tcp --dport 5000 -j ACCEPT
sudo iptables -I INPUT -p tcp --dport 9090 -j ACCEPT
flask run
