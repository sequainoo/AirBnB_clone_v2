#!/usr/bin/env bash
# setup web-server for web_static deployment
# create /data/web_static/releases/test/ and /data/web_static/shared/
# create a fake file in /data/web_static/releases/test/inde.html

# install nginx if not installed
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get -y install

# setup dir structure
sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared

# setup faek html
echo 'fake content' | sudo tee /data/web_static/releases/test/index.html

# create a symlink to /data/web_static/releases/test as current in /data/web_static/
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# change ownership of /data/ to ubuntu user and group
# -h --no-dereference in the case of symlink
sudo chown -hR ubuntu:ubuntu /data/

# update nginx config: /etc/nginx/sites-available/default
# to serve the content of /data/web_static/current/ to hbnb_static
# eg: http://mydomain.tech/hbnb_static
# config:
#       location /hbnb_static/ {
#               alias /data/web_static/current/;
#       }
CONFIG="\\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}"

sudo sed -i "/server_name _/a$CONFIG" /etc/nginx/sites-available/default

# restart nginx after config
sudo service nginx start
