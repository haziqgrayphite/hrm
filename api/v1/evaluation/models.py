import uuid
from django.db import models
from django.utils import timezone
from api.v1.accounts.models import CustomUser


class ParameterRating(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    score = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.score}"


class Parameter(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    comments = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BaseEvaluation(models.Model):
    evaluators = models.ManyToManyField(CustomUser, related_name="base_evaluation_evaluators")
    evaluatees = models.ManyToManyField(CustomUser, related_name="base_evaluation_evaluatees")
    parameters = models.ManyToManyField(Parameter, related_name="base_evaluation_parameter")

    valid_from = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()

    comment = models.CharField(max_length=500, blank=True, null=True)
    expiry_days = models.IntegerField(default=7, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_expired = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_expirable = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.is_expirable:
            if self.expiry_days is not None:
                if self.created_at is None:
                    self.created_at = timezone.now()
                self.valid_until = self.created_at + timezone.timedelta(days=self.expiry_days)
            else:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Base Evaluation ID: {self.id}, Valid from: {self.valid_from}, Valid until: {self.valid_until}"


class Evaluation(models.Model):
    evaluator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="evaluation_evaluator")
    evaluatee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="evaluation_evaluatee")
    parameters = models.ManyToManyField(Parameter, related_name="evaluation_parameters")

    comment = models.CharField(max_length=500, blank=True, null=True)
    expiry_days = models.IntegerField(blank=True, null=True)

    valid_from = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()

    is_active = models.BooleanField(default=True)
    is_evaluated = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_expirable = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.evaluator} -- {self.evaluatee}"


class EvaluationScore(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="evaluation_score")
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="evaluation_scores")
    parameter_rating = models.ForeignKey(ParameterRating, on_delete=models.CASCADE, related_name="evaluation_scores")

    is_active = models.BooleanField(default=True)
    is_evaluated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"EvaluationScore {self.id} - {self.parameter_rating}"
