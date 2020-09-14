from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from django.urls import reverse

from .utils import token_generator

User = get_user_model()


class CalendarQuerySet(models.QuerySet):
    def owned(self, request):
        if request.user.is_authenticated:
            return self.filter(owner=request.user)
        return self.none()

    def subscribed(self, request):
        if request.user.is_authenticated:
            return self.filter(subscribers__exact=request.user)
        return self.none()

    def available(self, request):
        if request.user.is_authenticated:
            return self.filter(Q(owner=request.user) | Q(subscribers__exact=request.user))
        return self.none()


class CalendarManager(models.Manager):
    def get_queryset(self):
        return CalendarQuerySet(self.model, using=self._db)

    def available(self, request):
        return self.get_queryset().available(request)

    def owned(self, request):
        return self.get_queryset().owned(request)


class Calendar(models.Model):
    name = models.CharField(max_length=200)
    overview = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True, default="#2222dd")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name="calendars", blank=True)
    # timezone

    objects = CalendarManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} owned by {self.owner}'

    def get_absolute_url(self):
        return reverse("cal:calendar_detail", kwargs={"pk": self.pk})


class EventManager(models.Manager):
    def owned(self, request):
        if request.user.is_authenticated:
            return self.filter(owner=request.user)
        return self.none()

    def available(self, request):
        return self.get_queryset().filter(calendar__in=Calendar.objects.available(request))

    def by_calendar(self, request, calendar_id):
        calendar = Calendar.objects.get(pk=calendar_id)
        if calendar in Calendar.objects.available(request):
            return self.get_queryset().filter(calendar=calendar)
        return self.get_queryset().none()


class Event(models.Model):
    name = models.CharField(max_length=200)
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=7, null=True, blank=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name="events")

    date = models.DateField()
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    whole_day = models.BooleanField(default=False)

    place = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    guests = models.ManyToManyField(User, through="Participation", related_name="as_guest_events", blank=True)

    objects = EventManager()

    # repeat
    # notification
    # timezone
    # guests permissions

    class Meta:
        order_with_respect_to = 'calendar'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cal:event_detail", kwargs={"pk": self.pk})


STATUS_CHOICES = (
    ('accept', 'Accepted'),
    ('perhaps', 'Perhaps'),
    ('rejected', 'Rejected'),
    ('none', 'No answer')
)


class Participation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='none')


class CalendarShareTokenManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(active=True)


class CalendarShareToken(models.Model):
    token = models.CharField(max_length=50, blank=True)
    calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE, related_name='share_token')
    active = models.BooleanField(default=False)

    objects = CalendarShareTokenManager()

    def __str__(self):
        return self.token

    def get_url(self, request=None):
        if request:
            return request.build_absolute_uri(reverse('cal:share_link', kwargs={'token': self.token}))
        return reverse('cal:share_link', kwargs={'token': self.token})


def share_token_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.active or not instance.token:
        instance.token = token_generator(instance)


pre_save.connect(share_token_pre_save_receiver, sender=CalendarShareToken)
