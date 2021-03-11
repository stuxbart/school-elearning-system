from celery import shared_task

from django.contrib.auth import get_user_model
from courses.emails import send_member_email


@shared_task
def send_added_to_course_confirmation_email(menbership_id):
    from courses.models import Membership
    membership = Membership.objects.get(id=menbership_id)
    send_member_email(menbership_id)
