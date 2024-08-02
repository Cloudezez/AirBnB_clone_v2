from fabric.api import local, put, run, env
from fabric.contrib.files import exists

# Set up the environment for Fabric
env.hosts = ['197.248.5.24']
env.user = 'ncmovers'
env.key_filename = 'my_ssh_private_key'

def do_deploy(archive_path):
    """Distributes an archive to web servers"""
    # Check if the archive exists locally
    if not exists(archive_path):
        print(f"Archive {archive_path} does not exist")
        return False

    try:
        # Upload the archive to /tmp/
        put(archive_path, '/tmp/')
        
        # Extract the filename without extension
        file_name = archive_path.split('/')[-1]
        file_name_no_ext = file_name.split('.')[0]
        
        # Create the release directory
        release_dir = f'/data/web_static/releases/{file_name_no_ext}/'
        run(f'mkdir -p {release_dir}')
        
        # Uncompress the archive
        run(f'tar -xzf /tmp/{file_name} -C {release_dir}')
        
        # Delete the archive from /tmp/
        run(f'rm /tmp/{file_name}')
        
        # Remove old symbolic link and create a new one
        run('rm -rf /data/web_static/current')
        run(f'ln -s {release_dir} /data/web_static/current')

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

