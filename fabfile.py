#!/usr/bn/python3
from fabric.api import *

env.hosts = ['ubuntu@web-01.onewazato.tech']

def do_print():
    run('ls -al')
