from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LeaveRequest, LeaveRequestTL, LeaveRequestHR, LeaveBalance, TeamLead


@receiver(post_save, sender=LeaveRequest)
def create_leave_request_tl(sender, instance, created, **kwargs):

    if created:
        is_team_lead_approval = False

        user = instance.user
        try:
            team_lead = TeamLead.objects.get(user=user)

            if team_lead:
                is_team_lead_approval = True

        except TeamLead.DoesNotExist:
            pass

        LeaveRequestTL.objects.create(
            leave_request=instance,
            is_team_lead_approval=is_team_lead_approval,
        )


@receiver(post_save, sender=LeaveRequestTL)
def update_leave_request_tl(sender, instance, **kwargs):

    if instance.is_team_lead_approval:
        instance.leave_request.is_team_lead_approval = True
        instance.leave_request.save()

        LeaveRequestHR.objects.create(
            leave_request=instance.leave_request,
            hr_comments="",
            is_hr_approval=False
        )


@receiver(post_save, sender=LeaveRequestHR)
def update_leave_balance(sender, instance, created, **kwargs):

    if not created:

        if instance.is_hr_approval:

            leave_request = instance.leave_request
            try:
                leave_balance = LeaveBalance.objects.get(employee=leave_request.user)

                if leave_request.sick_leave:
                    leave_balance.sick_leave_balance -= leave_request.leaves_required
                elif leave_request.annual_leave:
                    leave_balance.annual_leave_balance -= leave_request.leaves_required
                elif leave_request.casual_leave:
                    leave_balance.casual_leave_balance -= leave_request.leaves_required

                leave_balance.accumulative_balance -= leave_request.leaves_required
                leave_balance.save()

                leave_request.status = "Approved"
                leave_request.is_hr_approval = True
                leave_request.save()

            except LeaveBalance.DoesNotExist:
                pass
            except LeaveRequest.DoesNotExist:
                pass

        else:
            leave_request = instance.leave_request
            leave_request.status = "Rejected"
            leave_request.save()
