from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from ipware import get_client_ip
import settings
import logging


logger = logging.getLogger(settings.AUTH_LOGGING['LOGGER_NAME'])


def _get_ip(request):
    '''
    Returns the client IP, or '<unknown>'.
    '''
    client_ip, is_routable = get_client_ip(request)
    return client_ip or '<unknown>'


def _get_user(request):
    '''
    Returns a user attribute (e.g. username or email).
    '''
    return getattr(request.user, settings.AUTH_LOGGING['USER_ATTRIBUTE'])


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    '''
    Login signal handler.
    '''
    logger.info('User %s logged in from ip %s', _get_user(request), _get_ip(request))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    '''
    Logout signal handler.
    '''
    logger.info('User %s logged out from ip %s', _get_user(request), _get_ip(request))


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    '''
    Failed login attempt signal handler.
    '''
    if 'request' in kwargs:
        ip = _get_ip(kwargs['request'])
        logger.warning('Invalid login attempt from ip %s: %s', ip, credentials)
    else:
        logger.warning('Invalid login attempt: %s', credentials)
