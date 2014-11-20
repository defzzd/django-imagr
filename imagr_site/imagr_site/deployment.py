import os

def setup_deployment():
    # SECURITY WARNING: don't run with debug turned on in production!
    os,environ['DEBUG'] = False

    os.environ['ALLOWED_HOSTS'] = [
        "imagr_app.charlesgust.me",
    ]

    os.environ['STATIC_ROOT'] = "/var/imagr_app/charlesgust.me/static/"

    os.environ['MEDIA_ROOT'] = "/var/imagr_app/charlesgust.me/media/"

    # There is a risk that the greater security of setting
    #  these to True will not work unless we get an SSL
    #  certificate, and we don't know yet whether Amazon EC2
    #  will give us a certificate or let us use one of theirs

    os.environ['CSRF_COOKIE_SECURE'] = True

    os.environ['SESSION_COOKIE_SECURE'] = True

    # Performance Optimizations

    os.environ['CONN_MAX_AGE'] = 60
    # TEMPLATE_LOADERS =

    # Error reporting
