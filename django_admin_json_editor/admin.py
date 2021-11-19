import json

from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class JSONEditorWidget(forms.Widget):
    template_name = 'django_admin_json_editor/editor.html'

    def __init__(self, schema, collapsed=True, sceditor=False, editor_options=None):
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

        self._editor_options = {
            'theme': 'bootstrap4',
            'iconlib': 'fontawesome4',
        }
        self._editor_options.update(editor_options or {})

    def render(self, name, value, attrs=None, renderer=None):
        if callable(self._schema):
            schema = self._schema(self)
        else:
            schema = self._schema

        else:
            schema_choices = {}

        if 'options' not in schema:
            schema['options'] = {}

        schema['options']['collapsed'] = self._collapsed

        editor_options = self._editor_options.copy()
        editor_options['schema'] = schema

        context = {
            'name': name,
            'data': value,
            'editor_options': json.dumps(editor_options),
        }
        return mark_safe(render_to_string(self.template_name, context))

    @property
    def media(self):


        css = {
            'all': [
                'django_admin_json_editor/fontawesome/css/font-awesome.min.css',
                'django_admin_json_editor/style.css',
            ]
        }
        js = [
            'django_admin_json_editor/jsoneditor/jsoneditor.min.js',
        ]

        if self._editor_options['theme'] == 'bootstrap4':
            css['all'].append('django_admin_json_editor/bootstrap/css/bootstrap.min.css')
            js.append('django_admin_json_editor/jquery/jquery-3.5.1.slim.min.js')
            js.append('django_admin_json_editor/bootstrap/js/bootstrap.bundle.min.js')

        if self._sceditor:
            css['all'].append('django_admin_json_editor/sceditor/themes/default.min.css')
            js.append('django_admin_json_editor/sceditor/jquery.sceditor.bbcode.min.js')

        if self._default_options.get('template') == 'handlebars':
            js.append('django_admin_json_editor/handlebars/handlebars-v4.0.11.js')

        # Load our default Simple MDE files, but these can be overridden in django settings.
        css['all'] += conf.DAJE_SIMPLE_MDE_CSS
        js += conf.DAJE_SIMPLE_MDE_JS

        return forms.Media(css=css, js=js)
