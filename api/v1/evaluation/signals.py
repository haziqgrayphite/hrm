from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
from .models import Evaluation, BaseEvaluation


@receiver(post_save, sender=BaseEvaluation)
def create_evaluations(sender, instance, created, **kwargs):
    if created:
        evaluators = list(instance.evaluators.all())
        evaluatees = list(instance.evaluatees.all())
        parameters = list(instance.parameters.all())
        expiry_days = instance.expiry_days

        print("Signal handler triggered")
        print(f"Instance: {instance}")
        print(f"Evaluators: {evaluators}")
        print(f"Evaluatees: {evaluatees}")
        print(f"Parameters: {parameters}")
        print(f"Parameters: {expiry_days}")

        # Create Evaluation instances for each combination of evaluators, evaluatees, and parameters
        # for evaluator in evaluators:
        #     for evaluatee in evaluatees:
        #         for parameter in parameters:
        #             Evaluation.objects.create(
        #                 evaluator=evaluator,
        #                 evaluatee=evaluatee,
        #                 parameters=parameter,
        #                 is_active=True,
        #                 is_evaluated=False,
        #             )
