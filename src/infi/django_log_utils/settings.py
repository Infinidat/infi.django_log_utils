from django.conf import settings


# Settings for RequestDataLoggingMiddleware
REQUEST_DATA_LOGGING = dict(
    LOGGER_NAME='reqdata',
    USER_ATTRIBUTE='email',
    MAX_BODY_LENGTH=20000,
    SANITIZED_PARAMS=('password', 'secret')
)
REQUEST_DATA_LOGGING.update(getattr(settings, 'REQUEST_DATA_LOGGING', {}))


# Settings for SetUserHeaderMiddleware
SET_USER_HEADER = dict(
    USER_ATTRIBUTE='email'
)
SET_USER_HEADER.update(getattr(settings, 'SET_USER_HEADER', {}))


# Settings for auth signal handlers
AUTH_LOGGING = dict(
    LOGGER_NAME='auth',
    USER_ATTRIBUTE='email'
)
AUTH_LOGGING.update(getattr(settings, 'AUTH_LOGGING', {}))
