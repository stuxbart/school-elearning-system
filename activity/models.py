from django.db import models
from django.conf import settings

from courses.models import Course
from .signals import course_viewed_signal

User = settings.AUTH_USER_MODEL

# Create your models here.
class CourseViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} viewed {self.course}, {self.timestamp}"
    


def course_viewed_receiver(sender, course, request, *args, **kwargs):
    user = request.user
    if user.is_authenticated and user in course.participants.all():
        new_view_obj = CourseViewed.objects.create(
            user=user,
            course=course
        )
        print(new_view_obj.user, new_view_obj.course, new_view_obj.timestamp)


course_viewed_signal.connect(course_viewed_receiver)