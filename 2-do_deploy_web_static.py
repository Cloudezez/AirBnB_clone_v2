from fabric.api import env, put, run
import os

# Update with your server IPs and username
env.hosts = ['197.248.5.24']
env.user = 'ncmovers'
env.key_filename = './my_ssh_private_key'

def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
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

