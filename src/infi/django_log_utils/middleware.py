import logging
import json
from . import settings

# Django 1.10+ middleware compatibility
try:
    from django.utils.deprecation import MiddlewareMixin
except:
    class MiddlewareMixin(object):
        pass


class RequestDataLoggingMiddleware(MiddlewareMixin):

    logger = logging.getLogger(settings.REQUEST_DATA_LOGGING['LOGGER_NAME'])
    attribute = settings.REQUEST_DATA_LOGGING['USER_ATTRIBUTE']
    max_body_length = settings.REQUEST_DATA_LOGGING['MAX_BODY_LENGTH']
    sanitized_params = settings.REQUEST_DATA_LOGGING['SANITIZED_PARAMS']

    def process_request(self, request):
        if self.should_log(request):
            if request.POST:
                reqdata = self.querydict_reqdata(request.POST)
            elif request.META['CONTENT_TYPE'] == 'application/json':
                reqdata = self.json_reqdata(request.body)
            elif (request.body):
                reqdata = self.raw_reqdata(request.body)
            reqdata = reqdata.replace('\n', '\n    ')
            self.logger.info("(%s) %s %s\n    %s" % (
                self.get_user(request), request.method, request.get_full_path(), reqdata
            ))

    def should_log(self, request):
        return bool(request.body)

    def get_user(self, request):
        user = 'Anonymous'
        if hasattr(request, 'user') and not request.user.is_anonymous():
            user = getattr(request.user, self.attribute)
        return user

    def querydict_reqdata(self, querydict):
        lines = []
        for key, values in querydict.iterlists():
            if key in self.sanitized_params:
                values = ['********************']
            if len(values) == 1:
                lines.append('%s = "%s"' % (key, values[0]))
            else:
                values = ', '.join('"%s"' % v for v in values)
                lines.append('%s = [%s]' % (key, values))
        return '\n'.join(lines)

    def json_reqdata(self, data):
        try:
            data = json.loads(data)
        except:
            # Invalid json, log it as raw
            return self.raw_reqdata(data)
        if isinstance(data, dict):
            for key in self.sanitized_params:
                if key in data:
                    data[key] = '********************'
        return json.dumps(data, indent=4, ensure_ascii=False)

    def raw_reqdata(self, data):
        try:
            data = data.decode('utf-8')
        except:
            data = '* cannot decode *'
        if len(data) > self.max_body_length:
            data = "%s\n...\n" % data[0:self.max_body_length]
        return data


class SetUserHeaderMiddleware(MiddlewareMixin):
    '''
    Adds an X-User header to the response, identifying the authenticated user (or "-" for anonymous users).
    The motivation is to output the header's value in the NGINX log_format (use $sent_http_x_user).
    You should also remove it from the final reponse using the proxy_hide_header directive.
    '''

    attribute = settings.SET_USER_HEADER['USER_ATTRIBUTE']

    def process_response(self, request, response):
        user = '-'
        if hasattr(request, 'user') and not request.user.is_anonymous():
            user = getattr(request.user, self.attribute)
        response['X-User'] = user
        return response
