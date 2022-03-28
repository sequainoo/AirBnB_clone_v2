#!/usr/bin/python3
'''generartes a .tgz archive from the contents of web_static'''

from fabric.api import local
from time import strftime


def do_pack():
    '''packs web_static content into archive'''
    timenow = strftime("%Y%M%d%H%M%S")

    try:
        local('mkdir -p versions')
        filename = 'versions/web_static_{}.tgz'.format(timenow)
        local('tar -czvf {} web_static/'.format(filename))
        return filename
    except:
        return None
