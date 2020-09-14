from django.urls import path
from django.conf.urls import handler404

from .views import (
        CalendarListView,
        CalendarDetail,
        CalendarCreateView,
        CalendarEditView,
        CalendarDeleteView,
        CalendarShareView,
        CalendarDeleteSuccessView,
        CalendarEventsView,
        CalendarEventCreateView,
        EventUpdateView,
        EventDeleteView,
        EventDetailView,
        EventCreateView,
        ShareLinkView,
        CalendarRemoveSubscriberView,
        CalendarAddSubscriberView
    )

app_name = 'cal'

urlpatterns = [
    path('', CalendarListView.as_view(), name="calendar_list"),
    path('create/', CalendarCreateView.as_view(), name="calendar_create"),
    path('events/', CalendarEventsView.as_view(), name="m_calendar_events_list"),
    path('<int:pk>/', CalendarDetail.as_view(), name="calendar_detail"),
    path('<int:pk>/edit/', CalendarEditView.as_view(), name="calendar_edit"),
    path('<int:pk>/delete/', CalendarDeleteView.as_view(), name="calendar_delete"),
    path('<int:pk>/events/', CalendarEventsView.as_view(), name="calendar_events_list"),
    path('<int:pk>/share/', CalendarShareView.as_view(), name="calendar_share"),
    path('<int:pk>/subscribers/remove', CalendarRemoveSubscriberView.as_view(), name="calendar_remove_subscriber"),
    path('<int:pk>/subscribers/add', CalendarAddSubscriberView.as_view(), name="calendar_add_subscriber"),
    path('delete/success', CalendarDeleteSuccessView.as_view(), name="calendar_delete_success"),
    path('<int:pk>/events/create/', CalendarEventCreateView.as_view(), name="calendar_event_create"),
    path('event/create/', EventCreateView.as_view(), name="event_create"),
    path('event/<int:pk>/', EventDetailView.as_view(), name="event_detail"),
    path('event/<int:pk>/edit/', EventUpdateView.as_view(), name="event_edit"),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name="event_delete"),
    path('share/<token>/', ShareLinkView.as_view(), name="share_link")
]

handler404 = 'cal.views.handler404'
