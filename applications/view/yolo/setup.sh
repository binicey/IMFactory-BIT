#!/bin/bash
#打开外部端口 5000
sudo iptables -I INPUT -p tcp --dport 5001 -j ACCEPT
flask run
