#!/usr/bin/env python3
"""
Fabric script that creates and distributes an archive to your web servers.
"""

from fabric.api import local, put, run, env
from datetime import datetime
import os

env.hosts = ['197.248.5.24']
env.user = 'ncmovers'
env.key_filename = 'my_ssh_private_key'

def do_pack():
    """Generates a .tgz archive from the web_static folder."""
    time_now = datetime.now()
    archive_path = f"versions/web_static_{time_now.strftime('%Y%m%d%H%M%S')}.tgz"
    if not os.path.isdir("versions"):
        local("mkdir -p versions")
    result = local(f"tar -cvzf {archive_path} web_static", capture=True)
    if result.failed:
        return None
    return archive_path

def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    if not os.path.isfile(archive_path):
        return False

    try:
        # Upload archive
        put(archive_path, '/tmp/')
        
        # Extract file name without extension
        archive_name = os.path.basename(archive_path)
        file_name = archive_name.split(".")[0]
        
        # Create directory and extract archive
        run(f"mkdir -p /data/web_static/releases/{file_name}/")
        run(f"tar -xzf /tmp/{archive_name} -C /data/web_static/releases/{file_name}/")
        run(f"rm /tmp/{archive_name}")

        # Move contents and clean up
        run(f"mv /data/web_static/releases/{file_name}/web_static/* /data/web_static/releases/{file_name}/")
        run(f"rm -rf /data/web_static/releases/{file_name}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s /data/web_static/releases/{file_name}/ /data/web_static/current")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

def deploy():
    """Creates and deploys an archive."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

