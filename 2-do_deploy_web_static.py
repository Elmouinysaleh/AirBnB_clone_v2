#!/usr/bin/env python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
import os


# Set the username and SSH key
env.user = 'ubuntu'
env.key_filename = '/path/to/your/private/key.pem'

# Set the IP addresses of your web servers
env.hosts = ['52.55.249.213', '54.157.32.137']


def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the /data/web_static/releases/ directory
        filename = os.path.basename(archive_path)
        folder_name = "/data/web_static/releases/{}".format(os.path.splitext(filename)[0])
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))

        # Move the contents of the extracted folder to the desired location
        run("mv {}/web_static/* {}".format(folder_name, folder_name))

        # Remove the empty web_static folder
        run("rm -rf {}/web_static".format(folder_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current
        run("ln -s {} /data/web_static/current".format(folder_name))

        return True

    except Exception as e:
        print(str(e))
        return False
