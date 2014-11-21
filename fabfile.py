from fabric.api import task, cd, run, env, prompt, execute, sudo
from fabric.api import open_shell, settings, put
import os


def create_aws_env():
    env.hosts = ['localhost', '*']
    env['user'] = 'ubuntu'


def setup_env():
    sudo("apt-get -y update")
    sudo("apt-get -y install python-pip")
    sudo("apt-get -y install python-dev")
    sudo("apt-get -y install postgresql-9.3")
    sudo("apt-get -y install postgresql-server-dev-9.3")
    sudo("apt-get -y install git")
    sudo("apt-get -y install gunicorn")


def move_sources():
    run("git clone https://github.com/CharlesGust/django-imagr.git")
    cd("django-imagr")
    put("imagr_site/imagr_site/credentials.py",
       "imagr_site/imagr_site/credentials.py", use_sudo=True)

def install_pips():
    sudo("pip install -r requirements.txt")
    pass

# also, we need to sudo and bind on Ubuntu to get access to low number ports
# sudo(".....b0000")

# when copying using put(), first param is local machine,
#  second is remote, and third is use_sudo=True

# we will need this string to invoke gunicorn

def runserver():
    run('gunicorn imagr_site.wsgi:imagr_app')


@task
def run_complete_setup():
    create_aws_env()
    setup_env()
    move_sources()
    install_pips()
    runserver()
