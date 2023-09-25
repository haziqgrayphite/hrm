import uuid

from django.db import models
from django.utils import timezone

from api.v1.accounts.models import GrayphiteBaseModel, CustomUser


class ParameterRating(GrayphiteBaseModel):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.score}"


class Parameter(GrayphiteBaseModel):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    parameter_rating = models.ManyToManyField(ParameterRating, related_name="parameter_parameter_rating")

    def __str__(self):
        return self.name


class BaseEvaluation(GrayphiteBaseModel):

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

    def save(self, *args, **kwargs):
        if self.is_expirable:
            if self.expiry_days is not None:
                if self.created_at is None:
                    self.created_at = timezone.now()
                self.valid_until = self.created_at + timezone.timedelta(days=self.expiry_days)
            else:
                pass
        super().save(*args, **kwargs)


class Evaluation(GrayphiteBaseModel):
    evaluator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="evaluation_evaluator")
    evaluatee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="evaluation_evaluatee")
    parameters = models.ManyToManyField(Parameter, related_name="evaluation_parameters")

    is_active = models.BooleanField(default=True)
    is_evaluated = models.BooleanField(default=False)
