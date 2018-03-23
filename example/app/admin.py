from django.contrib import admin
from django import forms

from django_admin_json_editor import JSONEditorWidget

from .models import JSONModel, ArrayJSONModel, Tag, MultipleSchemaJSONModel

DATA_SCHEMA = {
    'type': 'object',
    'title': 'Data',
    'properties': {
        'text': {
            'title': 'Some text',
            'type': 'string',
            'format': 'textarea',
        },
        'status': {
            'title': 'Status',
            'type': 'boolean',
        },
        'html': {
            'title': 'HTML',
            'type': 'string',
            'format': 'html',
            'options': {
                'wysiwyg': 1,
            }
        },
    },
    'required': ['text']
}


def dynamic_schema(widget):
    return {
        'type': 'array',
        'title': 'roles',
        'items': {
            'type': 'object',
            'required': [
                'name',
                'tag',
            ],
            'properties': {
                'name': {
                    'title': 'Name',
                    'type': 'string',
                    'format': 'text',
                    'minLength': 1,
                },
                'tag': {
                    'title': 'Tag',
                    'type': 'string',
                    'enum': [i for i in Tag.objects.values_list('name', flat=True)],
                }
             }
        }
    }

SCHEMA_A = {
  "title": "Schema A",
  "type": "object",
  "options": {
    "disable_properties": True
  },
  "properties": {
    "schema_a": {
      "type": "array",
      "title": "FAQ-A",
      "uniqueItems": True,
      "items": {
        "type": "object",
        "title": "Category",
        "properties": {
          "title": {
            "type": "string"
          },
          "items": {
            "type": "array",
            "title": "Category Details",
            "items": {
              "type": "object",
              "title": "Item",
              "properties": {
                "title_for_a": {
                  "type": "string"
                },
                "description": {
                  "type": "string",
                  "format": "markdown"
                }
              }
            }
          }
        }
      }
    }
  }
}

SCHEMA_B = {
  "title": "Schema B",
  "type": "object",
  "properties": {
    "schema_b": {
      "type": "array",
      "title": "FAQ-B",
      "uniqueItems": True,
      "items": {
        "type": "object",
        "title": "Category",
        "properties": {
          "title": {
            "type": "string"
          },
          "items": {
            "type": "array",
            "title": "Category Details",
            "items": {
              "type": "object",
              "title": "Item",
              "properties": {
                "title_for_b": {
                  "type": "string"
                },
                "description": {
                  "type": "string",
                  "format": "markdown"
                }
              }
            }
          }
        }
      }
    }
  }
}

SCHEMA_C = {
  "title": "Lecture Slide Data",
  "type": "object",
  "properties": {
    "slide_show": {
      "type": "array",
      "title": "Slides",
      "uniqueItems": True,
      "items": {
        "type": "object",
        "title": "Slide",
        "headerTemplate": "{{#if self.title}}{{ i1 }} - {{ self.title }}{{else}}Slide {{ i1 }}{{/if}}",
        "properties": {
          "title": {
            "type": "string",
              "description": "Adding a title will include in the table of contents"
          },
          "markdown_a": {
            "type": "string",
            "format": "markdown"
          },
          "markdown_b": {
            "type": "string",
            "format": "markdown",
            "description": "Optional Markdown field for two column layouts"
          }
        }
      }
    }
  }
}

DATA_SCHEMA_CHOICES = {
    MultipleSchemaJSONModel.CATEGORY_A: SCHEMA_A,
    MultipleSchemaJSONModel.CATEGORY_B: SCHEMA_B,
    MultipleSchemaJSONModel.CATEGORY_C: SCHEMA_C
}


class JSONModelAdminForm(forms.ModelForm):
    class Meta:
        model = JSONModel
        fields = '__all__'
        widgets = {
            'data': JSONEditorWidget(DATA_SCHEMA, collapsed=False, sceditor=True),
        }

@admin.register(JSONModel)
class JSONModelAdmin(admin.ModelAdmin):
    form = JSONModelAdminForm


@admin.register(ArrayJSONModel)
class ArrayJSONModelAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        widget = JSONEditorWidget(dynamic_schema, False)
        form = super().get_form(request, obj, widgets={'roles': widget}, **kwargs)
        return form


@admin.register(MultipleSchemaJSONModel)
class MultipleSchemaJSONModelAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        # set default to the "first" one in the dict
        default_schema = DATA_SCHEMA_CHOICES[next(iter(DATA_SCHEMA_CHOICES))]
        if obj:
            # set the default schema_choice based on the category field.
            # this is needed so when an editing an existing object, the proper schema is used based on
            # the existing data
            try:
                default_schema = DATA_SCHEMA_CHOICES[obj.category]
            except KeyError:
                pass
        data_widget = JSONEditorWidget(default_schema, collapsed=False, sceditor=False,
                                       schema_choices=DATA_SCHEMA_CHOICES, schema_choice_field_name="category",
                                       default_options={"disable_properties": True, 'template': 'handlebars'})
        form = super().get_form(request, obj, widgets={'data': data_widget}, **kwargs)
        return form

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
