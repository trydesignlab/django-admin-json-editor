# Django Administration JSON Editor

[![Build Status](https://travis-ci.org/abogushov/django-admin-json-editor.svg?branch=master)](https://travis-ci.org/abogushov/django-admin-json-editor)

![Admin Json Editor](example/example.png)


Application adds support for editing JSONField in Django Administration via https://github.com/json-editor/json-editor.

## Quick start

Install application via pip:

```bash
pip install django-admin-json-editor
```

Add application to the INSTALLED_APPS settings:

```python
INSTALLED_APPS = [
    ...
    'django_admin_json_editor',
    ...
]
```

Define schema of json field:

```python
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
    },
}
```

Use JSONEditorWidget to bind editor to the form field:

```python
class JSONModelAdminForm(forms.ModelForm):
    class Meta:
        model = JSONModel
        fields = '__all__'
        widgets = {
            'data': JSONEditorWidget(DATA_SCHEMA, collapsed=False),
        }
```

### Dynamic schema

It is possible to build dynamic schema for widget:

```python
def dynamic_schema(widget):
    return {
        'type': 'array',
        'title': 'tags',
        'items': {
            'type': 'string',
            'enum': [i for i in Tag.objects.values_list('name', flat=True)],
        }
    }
```

```python
@admin.register(JSONModel)
class JSONModelAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        widget = JSONEditorWidget(dynamic_schema, False)
        form = super().get_form(request, obj, widgets={'tags': widget}, **kwargs)
        return form
```

### Multiple schemas

Its possible to define multiple schemas that change based off a select field.

example models.py
```python
class MultipleSchemaJSONModel(models.Model):
    CATEGORY_A, CATEGORY_B, CATEGORY_C = range(0, 3)
    CATEGORY_CHOICES = (
        (CATEGORY_A, 'Category A'),
        (CATEGORY_B, 'Category B'),
        (CATEGORY_C, 'Category C')
    )
    category = models.PositiveIntegerField(choices=CATEGORY_CHOICES, default=CATEGORY_A)
    data = JSONField()
```

admin.py

```python
# Define your schemas
SCHEMA_A = {
  "title": "Schema A",
  "type": "object",
  "properties": {
    "schema_a": {
      "type": "array",
      "title": "FAQ-A",
      "uniqueItems": True,
      "items": {
        "format": "table",
        "type": "object",
        "title": "Category",
        "properties": {
          "title": {
            "type": "string"
          },
          "items": {
            "type": "array",
            "title": "Category Details",
            "format": "table",
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
        "format": "table",
        "type": "object",
        "title": "Category",
        "properties": {
          "title": {
            "type": "string"
          },
          "items": {
            "type": "array",
            "title": "Category Details",
            "format": "table",
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
  "title": "Schema C",
  "type": "object",
  "properties": {
    "schema_c": {
      "type": "array",
      "title": "FAQ-C",
      "uniqueItems": True,
      "items": {
        "format": "table",
        "type": "object",
        "title": "Category",
        "properties": {
          "title": {
            "type": "string"
          },
          "items": {
            "type": "array",
            "title": "Category Details",
            "format": "table",
            "items": {
              "type": "object",
              "title": "Item",
              "properties": {
                "title_for_c": {
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

# Map category choices or other values to your schemas
DATA_SCHEMA_CHOICES = {
    MultipleSchemaJSONModel.CATEGORY_A: SCHEMA_A,
    MultipleSchemaJSONModel.CATEGORY_B: SCHEMA_B,
    MultipleSchemaJSONModel.CATEGORY_C: SCHEMA_C
}


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
                                       schema_choices=DATA_SCHEMA_CHOICES, schema_choice_field_name="category")
        form = super().get_form(request, obj, widgets={'data': data_widget}, **kwargs)
        return form
```

