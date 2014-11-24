import os

# This deployment.py file is specifically the version used for
# AWS EC2 instances. An additional deployment.py file may be substituted
# for it when running servers locally for development purposes.
# This file shout NOT contain sensitive information, such as passwords.


def setup_deployment():
    # SECURITY WARNING: don't run with debug turned on in production!
    os.environ['DEBUG'] = "False"
    os.environ['TEMPLATE_DEBUG'] = "False"

    # I think setting ALLOWED_HOSTS to '*' will only be secure if
    # gunicorn is running our Django app behind a proxy,
    # which is what Nginx is for. Nginx will be the thing that accepts
    # connections from a specific list of hosts (I think), and
    # that list is the AWS server's address we're running on.
    # The thing in the nginx.conf file that says:
    #   server_name *.amazonaws.com;
    # is what we thought we had to do here, but in fact it's not,
    # due to the whole proxy thing. So, here we're using '*' instead:
    os.environ['ALLOWED_HOSTS'] = ['*']  # "['imagr_app.charlesgust.me',]"

    # There is a risk that the greater security of setting
    #  these to True will not work unless we get an SSL
    #  certificate, and we don't know yet whether Amazon EC2
    #  will give us a certificate or let us use one of theirs

    os.environ['CSRF_COOKIE_SECURE'] = "True"

    os.environ['SESSION_COOKIE_SECURE'] = "True"

    # Performance Optimizations

    os.environ['CONN_MAX_AGE'] = "60"
    # TEMPLATE_LOADERS =

    # Error reporting
