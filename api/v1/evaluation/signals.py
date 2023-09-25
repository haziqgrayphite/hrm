from django.dispatch import receiver
from .models import Evaluation, BaseEvaluation
from django.db.models.signals import m2m_changed


@receiver(m2m_changed, sender=BaseEvaluation.parameters.through)
def create_evaluations(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add" and not reverse:

        evaluators = instance.evaluators.all()
        evaluatees = instance.evaluatees.all()
        parameters = instance.parameters.all()

        print("Signal handler triggered")
        print(f"Instance: {instance}")
        print(f"Evaluators: {evaluators}")
        print(f"Evaluatees: {evaluatees}")
        print(f"Parameters: {parameters}")

        for evaluator in evaluators:
            for evaluatee in evaluatees:
                evaluation_instance = Evaluation.objects.create(
                    evaluator=evaluator,
                    evaluatee=evaluatee,
                    is_active=True,
                    is_evaluated=False
                )
                evaluation_instance.parameters.set(parameters)
