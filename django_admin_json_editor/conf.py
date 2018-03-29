from django.conf import settings


class Settings(object):
    """
    Shadow Django's settings with a little logic
    """

    @property
    def DAJE_SIMPLE_MDE_CSS(self):
        return getattr(settings, 'DAJE_SIMPLE_MDE_CSS', ['django_admin_json_editor/simplemde/simplemde.min.css'])

    @property
    def DAJE_SIMPLE_MDE_JS(self):
        return getattr(settings, 'DAJE_SIMPLE_MDE_JS', ['django_admin_json_editor/simplemde/simplemde.min.js'])


conf = Settings()
