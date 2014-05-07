#!/usr/bin/env python

"""
This fab file to run a series of remote commands on a group of servers you specify.
You can query info, run remote commands etc in real time.
usage:
fab -f fab_log_parallel.py -R www log
"""

import os
import sys
import pprint
# NOTE: This is where you put your core.py file to have all of your role
# definitions, etc
from beconfigs.core import *
from fabric.api import *
from fabric.contrib.files import exists

# Need to do a workaround for this. All servers in known_hosts should be fixed. This is caused by all of the dns changes made over the years
#env.disable_known_hosts = True

"""
tail log file.
usage:
fab -R besearch log:log_file="~search/../logs/search.log"
"""


@task
@parallel(pool_size=10)
def log(log_file='/var/log/secure'):
    assert(env.remote_interrupt, env.sudo_user == FABRIC_USER)
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

"""
Get server load info
usage:
fab -R besearch who
"""


@task
@parallel(pool_size=10)
def who():
    assert(env.remote_interrupt)
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
        sudo("w", pty=True)  # prints 'mysql'

"""
Run tcpdump on server to see incoming packets
usage:
fab -R besearch tcp_dump:port_num="9200"
"""


@task
@parallel(pool_size=10)
def tcp_dump(port_num='9200'):
    assert(env.remote_interrupt)
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
        sudo("tcpdump -nni any 'port %s'" % (port_num))

"""
Run rpm -qa on server to see installed packages. You can pass in regex
usage:
fab -R besearch rpm_qa:package_name='openssl'
"""


@task
def rpm_qa(package_name='openssh'):
    assert(env.remote_interrupt)
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

"""
Run summary on server to see all info you need after fabric has run a given task on all the servers you specified
usage:
fab -R besearch summary:call_task='rpm_qa',package_name='openssh'
"""


@task
@runs_once
def summary(call_task='rpm_qa'):
    assert(env.remote_interrupt)
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

"""
Run node_list on workstation to get an updated list of which nodes are in chef
usage:
fab node_list:pattern='benet'
"""


@task
@roles('chef')
def node_list(pattern=''):
    assert(env.remote_interrupt)
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
        with cd(CHEF_WORKSTATION_DIR):
            return run('knife node list -F json')


@task
@runs_once
def parse_nodes(pattern=''):
    assert(env.remote_interrupt)
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
        results = execute(node_list)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(results)


"""
Run strace_debug script on server what a specific process is doing.
This handles the creation of the debug dir etc.
usage:
fab -R besearch strace_debug:process="httpd"
"""


@task
@parallel(pool_size=10)
def strace_debug(script_path='~/dev/behanceops/scripts', process='httpd'):
    assert(env.remote_interrupt)
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
        run('mkdir -p /tmp/strace_debug')
        put(script_path, '/tmp/strace_debug/strace_debug.sh', mode=0755)
        sudo("sudo bash /tmp/strace_debug/strace_debug.sh %s" % (process))

"""
Run node_list on workstation to get an updated list of which nodes are in chef
usage:
fab node_list:pattern='benet'
"""


@task
@roles('bescarlett')
def add_chef_key(clocal_path=FABRIC_CHEF_SECURE_LOCAL_PATH,
                 cremote_path=FABRIC_CHEF_SECURE_REMOTE_PATH,
                 cremote_file=FABRIC_CHEF_REMOTE_FILE,
                 clocal_file=FABRIC_CHEF_LOCAL_FILE,
                 dryrun=True):
    assert(env.remote_interrupt)
    with settings(
        hide('warnings'),
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
        if dryrun:
            with cd('opt'):
                run("file %s" % (cremote_path))
                print "pretend to get local file: %s" % (clocal_path)
                print "pretend to get remote folder %s" % (cremote_path)
                print "pretend to get remote file %s" % (cremote_file)
        else:
            with cd('/opt'):
                sudo("sudo mkdir -p %s" % (cremote_path), pty=True)
                with cd("%s" % (cremote_path)):
                    put(clocal_file,
                        "/tmp/be_chef_key",
                        mode=0600,
                        use_sudo=True)
                    sudo("sudo chown root:root /tmp/be_chef_key")
                    sudo("sudo mv /tmp/be_chef_key %s" % (cremote_file))
                    return sudo("sudo ls -lta %s" % (cremote_file), pty=True)
"""
Run strace_debug script on server what a specific process is doing.
This handles the creation of the debug dir etc.
usage:
fab -R beimage chef_client:why_run=True
"""
@task
@parallel(pool_size=3)
def chef_client(why_run="True"):
    assert(env.remote_interrupt)
    with settings(
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
      if why_run == "True":
          sudo("sudo chef-client --why-run", pty=True)
      else:
          sudo("sudo chef-client", pty=True)

