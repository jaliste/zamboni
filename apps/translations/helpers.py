from django.conf import settings
from django.utils import translation

import jinja2

from jingo import register


@register.filter
def locale_html(translatedfield):
    """HTML attributes for languages different than the site language"""
    if not translatedfield:
        return ''

    site_locale = translation.to_locale(translation.get_language())
    locale = translation.to_locale(translatedfield.locale)
    if locale == site_locale:
        return ''
    else:
        rtl_locales = map(translation.to_locale, settings.RTL_LANGUAGES)
        textdir = 'rtl' if locale in rtl_locales else 'ltr'
        return jinja2.Markup(' lang="%s" dir="%s"' % (translatedfield.locale,
                                                      textdir))


@register.filter
def truncate(s, length=255, killwords=False, end='...'):
    """
    Wrapper for jinja's truncate that checks if the object has a
    __truncate__ attribute first.
    """
    if s is None:
        return ''
    if hasattr(s, '__truncate__'):
        return s.__truncate__(length, killwords, end)
    return jinja2.filters.do_truncate(s, length, killwords, end)
