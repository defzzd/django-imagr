django-imagr
============

This was produced by Charlie Rode, Ben Friedland, and Charles Gust

(django-imagr)~/Documents/projects/django-imagr/django-imagr[models_cmg*]$ sudo -u postgres psql -U postgres postgres
psql (9.3.5)
Type "help" for help.

postgres=# CREATE DATABASE imagr;
CREATE DATABASE
postgres=# ALTER database imagr OWNER to imagr;
ERROR:  role "imagr" does not exist
postgres=# CREATE role imagr login password 'imagr'
postgres-# ;
CREATE ROLE
postgres=# ALTER database imagr OWNER to imagr;
ALTER DATABASE
postgres=# \l
