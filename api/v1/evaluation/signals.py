from django.dispatch import receiver
from .models import Evaluation, BaseEvaluation, EvaluationScore, ParameterRating
from django.db.models.signals import m2m_changed


@receiver(m2m_changed, sender=BaseEvaluation.parameters.through)
def create_evaluations(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add" and not reverse:

        evaluators = instance.evaluators.all()
        evaluatees = instance.evaluatees.all()
        parameters = instance.parameters.all()

        default_parameter_rating, _ = ParameterRating.objects.get_or_create(name="Default",
                                                                            defaults={"score": 0})
        evaluations = []

        for evaluator in evaluators:

            for evaluatee in evaluatees:

                evaluation_instance = Evaluation.objects.create(
                    evaluator=evaluator,
                    evaluatee=evaluatee,
                    is_active=True,
                    is_evaluated=False,
                )

                evaluation_instance.parameters.set(parameters)
                evaluations.append(evaluation_instance)

        for _evaluation in evaluations:
            for _parameter in parameters:

                _ = EvaluationScore.objects.create(
                    evaluation=_evaluation,
                    parameter=_parameter,
                    parameter_rating=default_parameter_rating
                )
