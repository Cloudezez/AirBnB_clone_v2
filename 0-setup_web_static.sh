#!/usr/bin/env bash
# This script sets up the web servers for the deployment of web_static

# Exit on error
set -e

# Install Nginx if it is not already installed
if ! dpkg -s nginx >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create the required directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file to test the Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link, removing the existing one if it exists
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R Cloudezez@Jaddy /data/

# Update the Nginx configuration to serve the content
nginx_config="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static/" "$nginx_config"; then
    sudo sed -i '/server_name _;/a \\n    location /hbnb_static/ {\n        alias /data/web_static/current/;\n    }\n' "$nginx_config"
fi

# Restart Nginx to apply the changes
sudo service nginx restart

# Exit successfully
exit 0

