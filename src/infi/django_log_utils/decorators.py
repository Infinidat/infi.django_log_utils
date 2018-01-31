from django.core.exceptions import NON_FIELD_ERRORS
import logging

logger = logging.getLogger()


def _format_one(error_dict):
    output = []
    for field, errors in error_dict.items():
        prefix = '' if field == NON_FIELD_ERRORS else field + ' - '
        for error in errors:
            output.append(prefix + error)
    return '\n'.join(output)


def _format_errors(form):
    if isinstance(form.errors, list):
        # This is a formset
        return '\n'.join([_format_one(e) for e in [form.non_form_errors()] + form.errors if e])
    # Regular form
    return _format_one(form.errors)


def log_validation_errors(form_cls):
    '''
    Decorate a form or a formset with this decorator to log all validation errors.
    '''
    orig_full_clean = getattr(form_cls, 'full_clean')
    def _full_clean_and_log(self):
        orig_full_clean(self)
        if self.errors:
            errors = _format_errors(self).replace('\n', '\n    ')
            logger.info('Validation errors in %s:\n    %s', form_cls.__name__, errors)
    setattr(form_cls, 'full_clean', _full_clean_and_log)
    return form_cls
