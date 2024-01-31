#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to web servers
"""
import os.path
from datetime import datetime
from fabric.api import env, put, run
from fabric.contrib import files

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_pack():
    """Creates a compressed archive of the web_static folder"""
    dt_now = datetime.now().strftime("%Y%m%d%H%M%S")
    local("mkdir -p versions")
    path = "versions/web_static_{}.tgz".format(dt_now)
    cmd = "tar -cvzf {} web_static".format(path)
    if local(cmd).succeeded:
        return path
    else:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not files.exists(archive_path):
        return False

    file = os.path.basename(archive_path)
    name = os.path.splitext(file)[0]

    try:
        put(archive_path, "/tmp/{}".format(file))
        run("mkdir -p /data/web_static/releases/{}/".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name))
        run("rm /tmp/{}".format(file))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
