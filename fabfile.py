
# All quoted comments and almost all of the code is from
# of Cris Ewing's tutorial:
# http://codefellows.github.io/
#      python-dev-accelerator/assignments/day12/fabric.html

# All the non-decorated functions in this file can be invoked
# as arguments to fab from the command line.

# "Let's start by creating a very simple test Python function
# we can use to show how fabric works in general."
from fabric.api import run


def host_type():
    run('uname -s')

# "Once you've saved this, the name of the new Python function becomes
# available as a subcommand for the fab command:"
#       fab -H localhost host_type
# ((note: the early tutorial steps here will require user login b/c no sudo))

# ...

# "Notice that you're local machine has prompted you to login with
# a password. That's a good thing. If you enable publickey login
# then fabric will skip this part for you. This also means that you
# won't be sending your password across a connection, so that's nice."


# "Having to specify a host to connect to is a bit awkward, so fabric
# provides a mechanism for setting this up automatically:"
from fabric.api import env
env.hosts = ['localhost']


# "Our interactions with boto are all oriented around
# creating and destroying servers.
# In fabric, our orientation will be toward
# manipulating a server once it exists.
# Before we do that, though we need to
# get a server running."

# Getting a connection to us-west-2:
import boto.ec2
env.aws_region = 'us-west-2'


def get_ec2_connection():
    if 'ec2' not in env:
        ec2_connection = boto.ec2.connect_to_region(env.aws_region)
        if ec2_connection is not None:
            env.ec2 = ec2_connection
            print("Connected to EC2 region {}".format(env.aws_region))
        else:
            raise IOError(
                "Unable to connect to EC2 region {}".format(env.aws_region))
    return env.ec2


import time


# "Arguments passed in from the command line appear in your function
# as strings. You are responsible for converting them if needed."
# Fabfile will run the following Python command using your command line args:
# provision_instance(wait_for_running, timeout, interval)
def provision_instance(wait_for_running=False, timeout=60, interval=2):
    wait_value = int(interval)
    timeout_value = int(timeout)
    connection = get_ec2_connection()
    # NOTE: Changing the following value can
    #       cost you money if you aren't careful.
    instance_type = 't1.micro'
    # This one is in your ~/.ssh dir:
    key_name = 'pk-aws'  # probably?? maybe not? ctrl-f tutorial's use of 'pk-'
    security_group = 'ssh-access'
    ami_id = 'ami-37501207'

    reservations = connection.run_instances(ami_id,
                                            key_name=key_name,
                                            instance_type=instance_type,
                                            security_groups=[security_group])

    new_instances = []
    for each_instance in reservations.instances:
        if each_instance.state == u'pending':
            new_instances.append(each_instance)
    running_instance = []
    if wait_for_running:
        time_waited = 0
        while new_instances and (time_waited < timeout_value):
            time.sleep(wait_value)
            time_waited += int(wait_value)
            for each_instance in new_instaces:
                current_state = each_instance.state
                print("Instance {} is currently {}".format(each_instance.id,
                                                           current_state))
                if current_state == "running":
                    running_instance.append(
                        new_instances.pop(new_instances.index(i)))  # !
                each_instance.update()

# Example use of above function:
# fab provision_instance:wait_for_running=1

# Example output:
# [localhost] Executing task 'provision_instance'
# Connected to EC2 region us-west-2
# Instance i-8c424a85 is pending
# Instance i-8c424a85 is pending
# Instance i-8c424a85 is pending
# Instance i-8c424a85 is pending
# Instance i-8c424a85 is pending
# Instance i-8c424a85 is pending
# Instance i-8c424a85 is pending
# Instance i-8c424a85 is running
# Done.

# "Once the function completes, you should be able to load your EC2
# dashboard and see the new instance you just created running happily."


# "When you execute a function using fabric, it is actually run repeatedly,
# once for each host you list in the env.hosts environment setting.
# At the moment, our script lists 'localhost', but we don't actually want
# to run this command on 'localhost', so we need to get around this.
# We could add a new host into the list, but that would require our
# knowing the name of the host ahead of time.
# Moreover, it would still mean that the commands were run both
# on localhost and this new remote host. That's no good."

# "Fabric provides the execute command specifically for this purpose.
# We can pass it the list of hosts on which we want to run a particular
# command, and it will do so for us. This means that we can dynamically
# set the name of the instance we want, and fabric will execute
# our chosen command on that server only!"

# "In order to play with that, though, we need to interactively select the
# instance we want to use (after all, we might have more than one, right?).
# We'll begin by building a function that allows us to list instances,
# optionally filtering for a particular state."

# NOTE: When list_aws_instances is not given :verbose=1, it will not print
#       anything about instances; it is used to prep for another function.
def list_aws_instances(verbose=False, state='all'):
    ec2_connection = get_ec2_connection()
    reservations = ec2_connection.get_all_reservations()
    instances = []
    for each_reservation in reservations:
        for each_instance in each_reservation.instances:
            if state == 'all' or each_instance.state == state:
                each_instance = {
                    'id': each_instance.id,
                    'type': each_instance.instance_type,
                    'image': each_instance.image_id,
                    'state': each_instance.state,
                    'instance': each_instance,
                }
                instances.append(each_instance)  # !
    env.instances = instances
    if verbose:
        import pprint
        pprint.pprint(env.instances)

# Example use of above function:
# fab list_aws_instances:verbose=1,state=running

# Example output:
# [localhost] Executing task 'list_aws_instances'
# Connected to EC2 region us-west-2
# [{'id': u'i-ab5159a2',
#   'image': u'ami-d0d8b8e0',
#   'instance': Instance:i-ab5159a2,
#   'state': u'running',
#   'type': u't1.micro'}]
# Done.


# "Now we must create a function that will take the output of that
# function and give us an interactive choice of running instances
# on which to take a given action. Fabric provides prompt,
# a function which will ask for input from the user at run time."
from fabric.api import prompt


# "Here, we build a list of the available instances that are 'running',
# and then ask the user to choose among them.
def select_instance(state='running'):
    # If there is no active instance, exit the function:
    if env.get('active_instance', False):
        return

    list_aws_instances(state=state)

    prompt_text = "Please select from the following instances:\n"
    # NOTE: The following syntax does different stuff from {} and .format()
    instance_printing_template = " %(ct)d: %(state)s instance %(id)s\n"
    for idx, instance in enumerate(env.instances):
        ct = idx + 1
        args = {'ct': ct}
        args.update(instance)
        prompt_text += instance_printing_template % args
    prompt_text += "Choose an instance: "

    def validation(input):
        choice = int(input)
        if choice not in range(1, (len(env.instances) + 1)):
            raise ValueError("{} is not a valid instance.".format(choice))
        else:
            return choice

    choice = prompt(prompt_text, validate=validation)
    # "After a valid choice is made, we can then hang that instance
    # on our env so that we can access it from other functions:"
    env.active_instance = env.instances[choice - 1]['instance']

# "Now, let's set up a function that will run a given command
# (passed by name as an argument) on the server we select:"
from fabric.api import execute


def run_command_on_selected_server(command):
    # Ask the user to select an instance:
    select_instance()
    # Build a list of hosts, including the server (always ubuntu for us):
    # (This is what Charles and I had a hard time finding due to AWS subnets!)
    selected_hosts = [
        'ubuntu@' + env.active_instance.public_dns_name
    ]
    # Execute the command:
    execute(command, hosts=selected_hosts)

# "Remember, you cannot use password authentication to log into AWS servers.
# If you find that you are prompted to enter a password in order to run
# this command on your remote server, it means you have some work to do."


# "In order to run a command on this server, you need to ensure that
# the keypair you set up for your AWS instances is available to the ssh agent.
# You can do that at the system level on your local machine:
#       ssh-add ~/.ssh/pk-aws.pem
# Now your local ssh agent knows that this is a file you might use
# to connect. When the AWS server asks to use public-key authentication,
# the agent will then try this key along with any others the agent
# knows about. If no known key works, ssh will bomb out."


# "execute() will take the name of a fabric command to run.
# We need a command that it will run that will install nginx
# for us and then start it:"
from fabric.api import sudo


# An internal command that should be wrapped for fab:
def _install_nginx():
    sudo('apt-get install nginx')
    # This command runs nginx with the start arg:
    sudo('/etc/init.d/nginx start')


# "Finally, we need to wrap this function in a function we might call
# from the command line that will run it on the server we select:""
def install_nginx():
    run_command_on_selected_server(_install_nginx)

# "Now, if we run this fabric command from our command line,
# we can get nginx installed on our AWS instance:
#       Executing task 'install_nginx'
#       Connected to EC2 region us-west-2
#       Please select from the following instances:
#        1: running instance i-ab5159a2
#       Choose an instance: 1
#       Executing task '_install_nginx'
#       sudo: apt-get install nginx
#       out: Setting up nginx-full (1.1.19-1ubuntu0.5) ...
#       out: Setting up nginx (1.1.19-1ubuntu0.5) ...
#       out: Processing triggers for libc-bin ...
#       out: ldconfig deferred processing now taking place
#       Done.
# At this point, you should be able to open a web browser and point
# it at your EC2 instance and see the default nginx web page.
# Remember, the public_dns_name of your instance is the way to get at it,
# so use that in your browser:
#       http://ec2-54-185-44-188.us-west-2.compute.amazonaws.com
# Challenge yourself to add two more functions:
#       1. Select a running instance to stop,
#           and then stop it with boto
#       2. Select a stopped instance to terminate,
#           and then terminate it with boto"


def stop_running_instance():
    # This code is from:
    #    https://github.com/miracode/django-imagr/blob/master/fabfile.py
    # I tried to find a way to do this using run_command_on_selected_server(),
    # but miracode's example turned out to be the way to go.
    # This is because the various commands store things in fabric's env
    # rather than passing them as parameters, which threw me through a
    # loop at first. Printing the state of the dictionary as things run
    # might help visualize this if your future fabfiles get longer.

    # Have the user place an instance selection in the env:
    select_instance()

    # Acquire a connection. Should done in this instance rather than
    # relying on the fact that select_instance() calls list_aws_instances().
    # It might be technically possible to place a connection in the env,
    # but I'd prefer to keep them function-scoped.
    ec2_connection = get_ec2_connection()

    # This command is too simple to require execute:
    ec2_connection.stop_instances(instance_ids=[env.active_instance.id])


# Similarly to stop_running_instance(), this function will not be
# effectively chained further up than select_instance().
def terminate_stopped_instance():
    # This code is also from:
    #    https://github.com/miracode/django-imagr/blob/master/fabfile.py

    select_instance(state='stopped')

    ec2_connection = get_ec2_connection()

    ec2_connection.terminate_instances(instance_ids=[env.active_instance.id])
