#!/usr/bin/env python

"""
This recipe will read logs from several servers in parallel in real time
usage:
fab -f fab_log_parallel.py -R www log
"""

import os
import sys
from fabric.api import *

FABRIC_KEY_FILENAME = os.environ.get('FABRIC_KEY_FILENAME')
FABRIC_JUMPSERVER   = os.environ.get('FABRIC_JUMPSERVER')
FABRIC_USER         = os.environ.get('FABRIC_USER')

env.roledefs = {
    # production servers
    'beesdata': [
      'beesdata41.be.net',
      'beesdata42.be.net',
      #'beesdata43.be.net',
      #'beesdata44.be.net',
      #'beesdata45.be.net',
      #'beesdata46.be.net',
      #'beesdata47.be.net',
      #'beesdata48.be.net',
      'beesdata49.be.net',
      #'beesdata50.be.net',
      #'beesdata51.be.net',
      'beesdata52.be.net',
      'beesdata53.be.net',
      'beesdata54.be.net',
      'beesdata55.be.net',
      'beesdata56.be.net',
      'beesdata57.be.net',
      'beesdata58.be.net'
    ],
    'besearch': [
      'besearch1.be.net',
      'besearch2.be.net',
      'besearch3.be.net',
      'besearch4.be.net',
      'besearch5.be.net',
      'besearch6.be.net'
    ]
}

env.remote_interrupt = True
env.LOG              = '/var/log/httpd/access_log'
env.use_ssh_config   = True
env.gateway          = FABRIC_JUMPSERVER
env.forward_agent    = True
env.keepalive        = 60
env.key_filename     = FABRIC_KEY_FILENAME
env.parallel         = True
env.sudo_user        = FABRIC_USER
env.user             = FABRIC_USER
env.remote_interrupt = True

# new stuff i'm adding
#env.abort_on_prompts = False

# Need to do a workaround for this. All servers in known_hosts should be fixed. This is caused by all of the dns changes made over the years
#env.disable_known_hosts = True


@parallel
def log(log_file='/var/log/secure'):
    assert(env.remote_interrupt == True,env.sudo_user=="bossjones")
    with settings(
      hide('warnings', 'running', 'stderr'),
      parallel=True,
      gateway=FABRIC_JUMPSERVER,
      use_ssh_config=True,
      forward_agent=True,
      key_filename=FABRIC_KEY_FILENAME,
      user=FABRIC_USER,
      sudo_user=FABRIC_USER,
      remote_interrupt=True,
      keepalive=60,
      warn_only=True
      ):
        sudo("sudo tail -f " + log_file, pty=True)

@parallel
def who():
    assert(env.remote_interrupt == True)
    with settings(
      hide('warnings', 'running', 'stderr'),
      parallel=True,
      gateway=FABRIC_JUMPSERVER,
      use_ssh_config=True,
      forward_agent=True,
      key_filename=FABRIC_KEY_FILENAME,
      user=FABRIC_USER,
      sudo_user=FABRIC_USER,
      remote_interrupt=True,
      keepalive=60,
      warn_only=True
      ):
        sudo("w", pty=True) # prints 'mysql'

@parallel
def tcp_dump():
    assert(env.remote_interrupt == True)
    with settings(
      hide('warnings', 'running', 'stderr'),
      parallel=True,
      gateway=FABRIC_JUMPSERVER,
      use_ssh_config=True,
      forward_agent=True,
      key_filename=FABRIC_KEY_FILENAME,
      user=FABRIC_USER,
      sudo_user=FABRIC_USER,
      remote_interrupt=True,
      keepalive=60,
      warn_only=True
      ):
        sudo("tcpdump -nni any 'port 9200'")

