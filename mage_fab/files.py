""" Module for providing helper methods for files within fabric """
from fabric.api import run


def readlink(path):
    """ Get the value of a symbolic link or canonical file name.
        See the readlink GNU documentation. If readlink returns an
        error a blank string is returned.
    """
    return run("readlink {0} || /bin/true".format(path))
