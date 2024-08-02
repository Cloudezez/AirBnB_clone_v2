from fabric.api import env
from fabric.operations import local
from fabric.api import put, run
import os
from datetime import datetime

# Update with your server IP and username
env.hosts = ['197.248.5.24']
env.user = '<ncmovers>'
env.key_filename = './my_ssh_private_key'  # Path to your SSH key

def do_pack():
    """Creates a .tgz archive from the web_static folder."""
    time_now = datetime.now()
    archive_name = "web_static_{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}.tgz".format(
        time_now.year, time_now.month, time_now.day, time_now.hour, time_now.minute, time_now.second
    )
    local("mkdir -p versions")
    result = local("tar -cvzf versions/{} web_static".format(archive_name), capture=True)

    if result.failed:
        return None
    return "versions/{}".format(archive_name)

def do_deploy(archive_path):
    """Deploys the archive to the web servers."""
    if not os.path.exists(archive_path):
        return False

    # Extract the file name and base name
    file_name = os.path.basename(archive_path)
    base_name = file_name.split(".")[0]

    # Define remote paths
    remote_tmp_path = "/tmp/{}".format(file_name)
    remote_release_dir = "/data/web_static/releases/{}/".format(base_name)

    try:
        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, remote_tmp_path)

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
        run("mkdir -p {}".format(remote_release_dir))
        run("tar -xzf {} -C {}".format(remote_tmp_path, remote_release_dir))

        # Delete the archive from the web server
        run("rm {}".format(remote_tmp_path))

        # Move the files from the web_static folder to the release folder
        run("mv {0}web_static/* {0}".format(remote_release_dir))
        run("rm -rf {}web_static".format(remote_release_dir))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current on the web server
        run("ln -s {} /data/web_static/current".format(remote_release_dir))

        return True
    except:
        return False

def deploy():
    """Creates and distributes an archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)

