from django.db import models
from django.contrib.postgres.fields import JSONField


class JSONModel(models.Model):
    data = JSONField(default={
        'text': 'some text',
        'status': False,
        'html': '<h1>Default</h1>',
    })


class ArrayJSONModel(models.Model):
    roles = JSONField(default=[])


class MultipleSchemaJSONModel(models.Model):
    CATEGORY_A, CATEGORY_B, CATEGORY_C = range(0, 3)
    CATEGORY_CHOICES = (
        (CATEGORY_A, 'Category A'),
        (CATEGORY_B, 'Category B'),
        (CATEGORY_C, 'Category C')
    )
    category = models.PositiveIntegerField(choices=CATEGORY_CHOICES, default=CATEGORY_A)
    data = JSONField()


class Tag(models.Model):
    name = models.CharField('name', max_length=10)
