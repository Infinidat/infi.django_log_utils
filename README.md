Overview
========
This is a reusable Django app that provides various useful utilities related to logging.
It was tested under Python 2.7 and 3.5.

Usage
=====

## Logging authentication events

Add `infi.django_log_utils.apps.Config` to the list of `INSTALLED_APPS` to log every user login, logout or failed login attempt. For example:
```
WARNING 2018-01-18 07:29:31,963 Invalid login attempt: {'username': u'freddy', 'password': '********************'}
INFO 2018-01-18 07:55:05,879 User freddy@example.com logged in from ip 127.0.0.1
INFO 2018-01-18 07:55:44,592 User freddy@example.com logged out from ip 127.0.0.1
```

### Settings

You can configure the middleware in your settings file using a `AUTH_LOGGING` dictionary containing some or all of the configuration settings:
```python
AUTH_LOGGING = dict(
    LOGGER_NAME='auth',
    USER_ATTRIBUTE='email'
)
```
The available settings are:
- `LOGGER_NAME` - which logger to use for the output.
- `USER_ATTRIBUTE` - which user attribute to output (e.g. "email", "username" or "id").

## Logging data sent from the client

Add `infi.django_log_utils.middleware.RequestDataLoggingMiddleware` to the list of installed middleware classes, and it will log all the data the is sent via POST, PUT and PATCH requests. It is possible to sanitize sensitive fields from the output. For example:
```
INFO 2018-01-18 07:29:31,692 (Anonymous) POST /admin/login/?next=/admin/
    username = "admin"
    password = "********************"
    next = "/admin/"
```
In case of a JSON request body, it is logged in JSON format.  Other content types are logged as raw text.

### Settings

You can configure the middleware in your settings file using a `REQUEST_DATA_LOGGING` dictionary containing some or all of the configuration settings:
```python
REQUEST_DATA_LOGGING = dict(
    LOGGER_NAME='reqdata',
    USER_ATTRIBUTE='email',
    MAX_BODY_LENGTH=20000,
    SANITIZED_PARAMS=('password', 'secret')
)
```
The available settings are:
- `LOGGER_NAME` - which logger to use for the output.
- `USER_ATTRIBUTE` - which user attribute to output (e.g. "email", "username" or "id").
- `MAX_BODY_LENGTH` - maximum number of bytes to output for raw text.
- `SANITIZED_PARAMS` - names of fields to sanitize. Note that in JSON output, only keys in the top-level object are sanitized.

## Adding the logged-in user to the access log of NGINX

NGINX usually logs usernames for users who log in via HTTP Basic Auth, but is unaware of authentication that happens inside Django. When you add `infi.django_log_utils.middleware.SetUserHeaderMiddleware` to the list of installed middleware classes, it puts an `X-User` header in each response. Then, it is possible to output the header's value in NGINX: just create a custom log format that includes `$sent_http_x_user`, and use this log format in your reverse proxy settings. It is also a good idea to use the `proxy_hide_header` directive to scrub the `X-User` header from the response. Here are the relevant parts in the NGINX configuration:
```
log_format django '$remote_addr - $sent_http_x_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';

server {
    ...
    location / {
        proxy_pass http://127.0.0.1:8000;
        ...
        access_log /var/log/nginx/access.log django;
        proxy_hide_header X-User;
    }
}
```

### Settings

You can change which user attribute to put in the `X-User` header (e.g. "email", "username" or "id") by adding this to your settings file:
```python
SET_USER_HEADER = dict(
    USER_ATTRIBUTE='email'
)
```

## Logging form validation errors

Decorate a form or a formset with `log_validation_errors`, and all validation errors will be logged. For example:
```python
from infi.django_log_utils.decorators import log_validation_errors

@log_validation_errors
class NameForm(forms.Form):
    name = forms.CharField(max_length=30)
```
The output might look like this:
```
INFO 2018-01-18 08:03:22,006 Validation errors in NameForm:
    name - This field is required.
```

Development
===========

## Building the Project

Run the following commands:

    easy_install -U infi.projector
    projector devenv build --use-isolated-python

## Running the tests

The tests directory contains a demo Django project which is used for testing. To run the tests:

    cd src/tests
    ./manage.py test
