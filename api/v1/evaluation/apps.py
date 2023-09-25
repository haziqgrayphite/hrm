from django.apps import AppConfig


class EvaluationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.v1.evaluation'

    def ready(self):
        import api.v1.evaluation.signals


