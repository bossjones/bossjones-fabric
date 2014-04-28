#!/usr/bin/env python

"""
This recipe will read logs from several servers in parallel in real time
usage:
fab -f fab_log_parallel.py -R www log
"""

import os
import sys
from beconfigs.core import *
from fabric.api import *


# new stuff i'm adding
#env.abort_on_prompts = False

# Need to do a workaround for this. All servers in known_hosts should be fixed. This is caused by all of the dns changes made over the years
#env.disable_known_hosts = True

@task
@parallel
def log(log_file='/var/log/secure'):
    assert(env.remote_interrupt == True,env.sudo_user==FABRIC_USER)
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

@task
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

@task
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

@task
def rpm_qa(package_name='openssh'):
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
        return sudo('rpm -qa | grep "%s"' % (package_name))

@task
@runs_once
def summary(call_task='rpm_qa'):
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
        results = execute(call_task)
        print results

@task
@roles('chef')
def node_list(pattern=''):
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
        run('cd /home/%s && knife node list | grep "%s"' % (user,pattern))

