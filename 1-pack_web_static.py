#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the
web_static directory.
"""
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    Compresses the contents of the web_static directory into a .tgz archive.

    Returns:
        The file path of the generated archive, or None if archiving fails.
    """
    try:
        dt = datetime.utcnow()
        file_path = "versions/web_static_{}{}{}{}{}{}.tgz".format(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        )
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(file_path))
        return file_path
    except Exception:
        return None
