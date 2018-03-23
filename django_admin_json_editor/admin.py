import copy

import collections
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class JSONEditorWidget(forms.Widget):
    template_name = 'django_admin_json_editor/editor.html'

    def __init__(self, schema, collapsed=True, sceditor=False, schema_choices=False, schema_choice_field_name=False, default_options=False):
        super(JSONEditorWidget, self).__init__()
        self._schema = schema
        self._collapsed = collapsed
        self._sceditor = sceditor
        self._schema_choices = schema_choices
        self._schema_choice_field_name = schema_choice_field_name
        self._default_options = default_options if default_options else {}

        if schema_choices and schema_choice_field_name:
            if type(schema_choices) != dict:
                raise TypeError("schema_choices must be a dict, but type of \"%s\" was given" % type(schema_choices))
            if type(schema_choice_field_name) != str:
                raise TypeError("schema_choice_field_name must be a string, but type of \"%s\" was given" % type(schema_choice_field_name))
        elif (schema_choices and not schema_choice_field_name) or (schema_choice_field_name and not schema_choices):
            raise AttributeError("schema_choices and schema_choice_field_name must be supplied together.")

        if default_options and type(default_options) != dict:
            raise TypeError("default_options must be a dict, but type of \"%s\" was given" % type(default_options))

    def render(self, name, value, attrs=None, renderer=None):
        if callable(self._schema):
            schema = self._schema(self)
        else:
            schema = copy.copy(self._schema)

        if self._schema_choices:
            if callable(self._schema_choices):
                schema_choices = self._schema_choices(self)
            else:
                schema_choices = copy.copy(self._schema_choices)

        else:
            schema_choices = {}

        if 'options' not in schema:
            schema['options'] = {}

        schema['options']['collapsed'] = self._collapsed

        context = {
            'name': name,
            'schema': schema,
            'data': value,
            'sceditor': int(self._sceditor),
            'schema_choices': schema_choices,
            'schema_choice_field_name': self._schema_choice_field_name,
            'default_options': self._default_options
        }
        return mark_safe(render_to_string(self.template_name, context))

    @property
    def media(self):
        css = {
            'all': [
                'django_admin_json_editor/bootstrap/css/bootstrap.min.css',
                'django_admin_json_editor/fontawesome/css/font-awesome.min.css',
                'django_admin_json_editor/style.css',
                'django_admin_json_editor/simplemde/simplemde.min.css'
            ]
        }
        js = [
            'django_admin_json_editor/jquery/jquery.min.js',
            'django_admin_json_editor/bootstrap/js/bootstrap.min.js',
            'django_admin_json_editor/jsoneditor/jsoneditor.min.js',
            'django_admin_json_editor/simplemde/simplemde.min.js'
        ]
        if self._sceditor:
            css['all'].append('django_admin_json_editor/sceditor/themes/default.min.css')
            js.append('django_admin_json_editor/sceditor/jquery.sceditor.bbcode.min.js')

        if self._default_options.get('template') == 'handlebars':
            js.append('django_admin_json_editor/handlebars/handlebars-v4.0.11.js')

        return forms.Media(css=css, js=js)
