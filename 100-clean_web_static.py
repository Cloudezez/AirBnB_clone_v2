#!/usr/bin/env python3
"""
Fabric script to clean up old archives.
"""

from fabric.api import run, local, env
import os

env.hosts = ['197.248.5.24']
env.user = '<ncmovers'
env.key_filename = 'my_ssh_private_key'

def do_clean(number=0):
    """
    Deletes out-of-date archives.

    :param number: Number of recent archives to keep. 
                   If number is 0 or 1, only the most recent archive will be kept.
                   If number is 2, the most recent and the second most recent archives will be kept, etc.
    """
    # Local directory
    local_dir = "versions"
    
    # Get all archives
    local_archives = sorted([f for f in os.listdir(local_dir) if os.path.isfile(os.path.join(local_dir, f))])
    local_archives.sort(key=lambda x: os.path.getmtime(os.path.join(local_dir, x)), reverse=True)

    # Determine archives to keep
    if number == 0 or number == 1:
        number = 1
    else:
        number = int(number)
        
    archives_to_keep = local_archives[:number]
    archives_to_delete = local_archives[number:]

    # Delete old archives locally
    for archive in archives_to_delete:
        local(f"rm -f {os.path.join(local_dir, archive)}")
        print(f"Deleted local archive: {archive}")

    # Remote cleanup
    def clean_remote_archives():
        """
        Deletes old archives on the remote server.
        """
        # List of all archives
        result = run("ls -t /data/web_static/releases/")
        archives = result.split()
        
        # Determine archives to keep
        if number == 0 or number == 1:
            number = 1
        else:
            number = int(number)
        
        archives_to_keep = archives[:number]
        archives_to_delete = archives[number:]

        # Delete old archives remotely
        for archive in archives_to_delete:
            run(f"rm -rf /data/web_static/releases/{archive}")
            print(f"Deleted remote archive: {archive}")

    # Execute remote cleanup on all hosts
    for host in env.hosts:
        with env.host_string(host):
            clean_remote_archives()

