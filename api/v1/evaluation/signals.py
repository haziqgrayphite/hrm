from django.dispatch import receiver
from .models import Evaluation, BaseEvaluation, EvaluationScore, ParameterRating
from django.db.models.signals import m2m_changed


@receiver(m2m_changed, sender=BaseEvaluation.parameters.through)
def create_evaluations(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add" and not reverse:

        evaluators = instance.evaluators.all()
        evaluatees = instance.evaluatees.all()
        parameters = instance.parameters.all()

        expiry_days = instance.expiry_days
        comment = instance.comment
        valid_until = instance.valid_until
        valid_from = instance.valid_from

        is_active = instance.is_active
        is_expired = instance.is_expired
        is_completed = instance.is_completed
        is_expirable = instance.is_expirable

        default_parameter_rating, _ = ParameterRating.objects.get_or_create(
            name="Default",
            defaults={"score": 0}
        )
        evaluations = []

        for evaluator in evaluators:

            for evaluatee in evaluatees:

                evaluation_instance = Evaluation.objects.create(
                    evaluator=evaluator,
                    evaluatee=evaluatee,
                    expiry_days=expiry_days,
                    comment=comment,
                    is_active=is_active,
                    is_expired=is_expired,
                    is_completed=is_completed,
                    is_expirable=is_expirable,
                    valid_until=valid_until,
                    valid_from=valid_from
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
