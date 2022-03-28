#!/usr/bin/env bash
# script sets up a web server for deployement of web_static

# install nginx
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install nginx

# setup dir /data/ if not exist
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared

# a fake html file in test
echo 'Fake html doc content' | sudo tee /data/web_static/releases/test/index.html

# create a symbolic link to /test/
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# change ownership of /data/ and all subcontents to ubuntu
sudo chown -hR ubuntu:ubuntu /data/

# add to nginx configuration to serve from /data/web_static/current/ when
# requested /hbnb_static: use alias
CONFIG="\\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n"
sudo sed -i "/server_name _/a$CONFIG" /etc/nginx/sites-available/default

# restart nginx
sudo service nginx start
