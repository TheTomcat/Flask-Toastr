# -*- coding: utf-8 -*-
from jinja2 import Markup, Template
from flask import current_app, render_template, get_flashed_messages

class _toastr(object):
    @staticmethod
    def include_toastr_js(version='2.1.4', local_js=None):
        js = ''
        if local_js is not None:
            js = '<script src="%s"></script>\n' % local_js
        elif version is not None:
            js_filename = 'toastr.min.js'
            js = '<script src="//cdnjs.cloudflare.com/ajax/libs/' \
                 'toastr.js/%s/%s"></script>\n' % (version, js_filename)
        return Markup(js)

    @staticmethod
    def include_toastr_css(version='2.1.4', local_css=None):
        css = ''
        if local_css is not None:
            css = '<link href="%s" rel="stylesheet" />\n' % local_js
        elif version is not None:
            css_filename = 'toastr.min.css'
            css = '<link href="//cdnjs.cloudflare.com/ajax/libs/' \
                  'toastr.js/%s/%s" rel="stylesheet" />\n' % (version, css_filename)
        return Markup(css)

    @staticmethod
    def include_jquery(version='2.1.0', local_js=None):
        js = ''
        if local_js is not None:
            js = '<script src="%s"></script>\n' % local_js
        else:
            js = ('<script src="//code.jquery.com/' +
                  'jquery-%s.min.js"></script>') % version
        return Markup(js)

    @staticmethod
    def message():
        toastr_options = 'toastr.options.closeButton = %s; \
        toastr.options.timeOut = %s; \
        toastr.options.extendedTimeOut = %s; \
        toastr.options.positionClass = \"%s\"; \
        toastr.options.preventDuplicates = %s; \
        toastr.options.newestOnTop = %s; \
        toastr.options.progressBar = %s; ' % (
            current_app.config.get('TOASTR_CLOSE_BUTTON'),
            current_app.config.get('TOASTR_TIMEOUT'),
            current_app.config.get('TOASTR_EXTENDED_TIMEOUT'),
            current_app.config.get('TOASTR_POSITION_CLASS'),
            current_app.config.get('TOASTR_PREVENT_DUPLICATES'),
            current_app.config.get('TOASTR_NEWS_ON_TOP'),
            current_app.config.get('TOASTR_PROGRESS_BAR'))
        message = Template('''
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    <script type="text/javascript">
      (function($) {
        $(document).ready(function() {
          {{ toastr_options }}
          {% for category, message in messages|reverse %}
            {% if category is undefined or category == 'message' %}
              toastr.info(\'{{ message }}\', \'{{ category }}\')
            {% else %}
              toastr.{{ category }}(\'{{ message }}\', \'{{ category }}\')
            {% endif %}
          {% endfor %}
        });
      })(jQuery);
    </script>
  {% endif %}
{% endwith %}
''')
        return Markup(render_template(message,
            get_flashed_messages=get_flashed_messages,
            toastr_options=toastr_options))


class Toastr(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['toastr'] = _toastr
        app.context_processor(self.context_processor)

        app.config.setdefault('TOASTR_CLOSE_BUTTON', 'true')
        app.config.setdefault('TOASTR_TIMEOUT', 15000)
        app.config.setdefault('TOASTR_EXTENDED_TIMEOUT', 1000)
        app.config.setdefault('TOASTR_POSITION_CLASS', 'toast-top-right')
        app.config.setdefault('TOASTR_PREVENT_DUPLICATES', 'false')
        app.config.setdefault('TOASTR_NEWS_ON_TOP', 'false')
        app.config.setdefault('TOASTR_PROGRESS_BAR', 'true')

    @staticmethod
    def context_processor():
        return {
            'toastr': current_app.extensions['toastr']
        }

    def create(self, timestamp=None):
        return current_app.extensions['toastr'](timestamp)
