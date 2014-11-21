from fabric.api import run
from fabric.api import env
import boto.ec2
import time

env.aws_region = 'us-west-2'

env.hosts = ['localhost', ]

def host_type():
    run('uname -s')

def get_ec2_connection():
    if 'ec2' not in env:
        conn = boto.ec2.connect_to_region(env.aws_region)
        if conn is not None:
            env.ec2 = conn
            print "Connected to EC2"
        else:
            msg = "Unable to connect"
            raise IOError(msg)
    return env.ec2

def provision_instance 
