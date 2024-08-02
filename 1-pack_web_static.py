#!/usr/bin/python3
# This script generates a .tgz archive from the contents of the web_static folder
from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    # Create the versions directory if it doesn't exist
    if not os.path.exists('versions'):
        os.makedirs('versions')

    # Create the archive file name with the current date and time
    now = datetime.now()
    archive_name = "versions/web_static_{}.tgz".format(now.strftime("%Y%m%d%H%M%S"))

    # Create the archive
    result = local("tar -cvzf {} web_static".format(archive_name))

    # Check if the archive was created successfully and return the path
    if result.succeeded:
        return archive_name
    else:
        return None

