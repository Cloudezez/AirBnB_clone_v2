# Puppet manifest to set up the web_static directory structure

# Ensure the /data directory exists
file { '/data':
  ensure => directory,
}

# Ensure the /data/web_static directory exists
file { '/data/web_static':
  ensure => directory,
}

# Ensure the /data/web_static/releases directory exists
file { '/data/web_static/releases':
  ensure => directory,
}

# Ensure the /data/web_static/shared directory exists
file { '/data/web_static/shared':
  ensure => directory,
}

# Create a test index.html file in /data/web_static/releases/test
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n",
}

# Create a symbolic link from /data/web_static/current to /data/web_static/releases/test
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
}

# Configure nginx to serve the web_static directory
file { '/etc/nginx/sites-available/web_static':
  ensure  => file,
  content => "
server {
    listen 80;
    server_name localhost;

    location /hbnb_static/ {
        alias /data/web_static/current/;
    }
}
  ",
}

# Enable the nginx configuration
file { '/etc/nginx/sites-enabled/web_static':
  ensure => link,
  target => '/etc/nginx/sites-available/web_static',
  require => File['/etc/nginx/sites-available/web_static'],
}

# Ensure nginx is installed and running
package { 'nginx':
  ensure => installed,
}

service { 'nginx':
  ensure => running,
  enable => true,
  require => Package['nginx'],
}

