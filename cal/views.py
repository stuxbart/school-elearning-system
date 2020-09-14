import calendar
import datetime

from django.shortcuts import render, reverse, get_object_or_404, redirect, Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    View
)

from .models import Calendar, Event, CalendarShareToken
from .utils import create_url_from_date

User = get_user_model()


class CalendarListView(LoginRequiredMixin, ListView):
    template_name = 'cal/list.html'

    def get_queryset(self):
        return Calendar.objects.available(self.request)

    def get_context_data(self, **kwargs):
        context = super(CalendarListView, self).get_context_data(**kwargs)
        context['owned'] = context['object_list'].owned(self.request)
        context['subscribed'] = context['object_list'].subscribed(self.request)
        return context


class CalendarDetail(LoginRequiredMixin, DetailView):
    template_name = 'cal/detail.html'

    def get_queryset(self):
        return Calendar.objects.available(self.request)


class CalendarCreateView(LoginRequiredMixin, CreateView):
    model = Calendar
    template_name = 'cal/create.html'
    fields = ['name', 'overview', 'color']

    def get_success_url(self):
        return reverse('cal:calendar_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.token = None
        return super(CalendarCreateView, self).form_valid(form)


class CalendarEditView(LoginRequiredMixin, UpdateView):
    template_name = 'cal/edit.html'
    fields = ['name', 'overview', 'color']

    def get_queryset(self):
        return Calendar.objects.owned(self.request)

    def get_success_url(self):
        return reverse('cal:calendar_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form, *args, **kwargs):
        form.instance.owner = self.request.user
        return super(CalendarEditView, self).form_valid(form)


class CalendarDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "cal/delete.html"

    def get_queryset(self):
        return Calendar.objects.owned(self.request)

    def get_success_url(self):
        return reverse('cal:calendar_delete_success')


class CalendarDeleteSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'cal/delete_success.html'


class CalendarEventsView(LoginRequiredMixin, ListView):
    model = Event

    def get_queryset(self):
        pk = self.kwargs.get('pk') or None
        if pk is not None:
            qs = Event.objects.by_calendar(self.request, self.kwargs['pk'])
        else:
            qs = Event.objects.available(self.request)
        print(qs)
        fill = True
        now = datetime.datetime.now()

        day = self.request.GET.get('day') or None
        try:
            day = int(day)
            if not 1 <= day <= 31:
                day = None
        except ValueError:
            day = None
        except TypeError:
            day = None

        month = self.request.GET.get('month') or None
        try:
            month = int(month)
            if not 1 <= month <= 12:
                month = None
        except ValueError:
            month = None
        except TypeError:
            day = None

        if month is None and day is not None and fill:
            month = now.month
        elif month is None and day is not None:
            month = now.month  # default
            day = None  # default

        year = self.request.GET.get('year') or None
        try:
            year = int(year)
        except ValueError:
            year = None
        except TypeError:
            day = None

        if year is None and month is None and day is None:
            year = now.year  # default
            month = now.month  # default
            day = None  # default
        if year is None and fill:
            year = now.year
        elif year is None:
            year = now.year  # default
            month = now.month  # default
            day = None  # default

        self.kwargs['year'] = year
        self.kwargs['month'] = month
        self.kwargs['day'] = day

        qs = qs.filter(date__year=year) if year is not None else qs
        qs = qs.filter(date__month=month) if month is not None else qs
        qs = qs.filter(date__day=day) if day is not None else qs
        qs = qs.order_by('date__day')
        # .annotate(day=ExtractDay('date'))#.values('day', 'name').annotate(c=Count('day')).order_by()

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['day'] = self.kwargs['day']
        if self.kwargs['month']:
            context['days_list'] = calendar.monthcalendar(self.kwargs['year'], self.kwargs['month'])

        return context

    def get_template_names(self):
        kw = self.kwargs
        if kw['year'] is not None and kw['month'] is not None and kw['day'] is not None:
            template_name = 'cal/events/list_day.html'
        elif kw['year'] is not None and kw['month'] is not None:
            template_name = 'cal/events/list_month.html'
        elif kw['year'] is not None:
            template_name = 'cal/events/list_year.html'
        else:
            template_name = 'cal/events/list_month.html'
        return [template_name]


class CalendarEventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'body', 'color', 'date', 'start', 'end', 'whole_day', 'place', 'calendar']
    template_name = 'cal/events/create.html'

    def get_initial(self):
        initial = super().get_initial()
        cal = get_object_or_404(Calendar, pk=self.kwargs['pk'])
        initial['color'] = cal.color
        initial['calendar'] = cal
        return initial

    def get_success_url(self):
        base_url = reverse('cal:m_calendar_events_list')
        return f'{base_url}{create_url_from_date(self.object.date)}'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.calendar = get_object_or_404(Calendar, pk=self.kwargs['pk'])
        return super(CalendarEventCreateView, self).form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    fields = ['name', 'body', 'color', 'date', 'start', 'end', 'whole_day', 'place', 'calendar']
    template_name = 'cal/events/edit.html'

    def get_queryset(self):
        return Event.objects.owned(self.request)

    def get_success_url(self):
        base_url = reverse('cal:m_calendar_events_list')
        return f'{base_url}{create_url_from_date(self.object.date)}'


class EventDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'cal/events/delete.html'

    def get_success_url(self):
        return reverse('cal:calendar_delete_success')

    def get_queryset(self):
        return Event.objects.owned(self.request)


class EventDetailView(LoginRequiredMixin, DetailView):
    template_name = 'cal/events/detail.html'

    def get_queryset(self):
        return Event.objects.available(self.request)


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'body', 'color', 'date', 'start', 'end', 'whole_day', 'place', 'calendar']
    template_name = 'cal/events/create.html'

    def get_success_url(self):
        base_url = reverse('cal:m_calendar_events_list')
        return f'{base_url}{create_url_from_date(self.object.date)}'

    def form_valid(self, form):
        if form.instance.calendar.owner == self.request.user:
            form.instance.owner = self.request.user
            return super(EventCreateView, self).form_valid(form)
        else:
            raise PermissionDenied()


class CalendarShareView(LoginRequiredMixin, View):
    template_name = 'cal/share.html'

    def get(self, request, *args, **kwargs):
        cal = get_object_or_404(Calendar, pk=self.kwargs['pk'])
        token = CalendarShareToken.objects.filter(calendar=cal)
        context = {}
        if token.exists():
            if token.first().active:
                context['token'] = token.first()
                context['token_link'] = token.first().get_url(request)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        cal = get_object_or_404(Calendar, pk=self.kwargs['pk'])
        token_qs = CalendarShareToken.objects.filter(calendar=cal)

        if not token_qs.exists():
            token = CalendarShareToken.objects.create(calendar=cal, active=True)
            token.save()
        else:
            token = token_qs.first()
            t = request.POST.get('token') or None
            if t is not None:
                if t == token.token:
                    if token.active:
                        token.active = False
                        token.save()
                    token = None
                else:
                    token = None
            else:
                if not token.active:
                    token.active = True
                    token.save()
        context = {
            'token': token
        }
        if token:
            context['token_link'] = token.get_url(request)
        return render(request, self.template_name, context)


class ShareLinkView(LoginRequiredMixin, View):
    template_name = 'cal/subscribe.html'

    def get(self, request, *args, **kwargs):
        t = self.kwargs.get('token')
        token = CalendarShareToken.objects.get(token=t)
        cal = token.calendar
        if request.user in cal.subscribers.all() or request.user == cal.owner:
            return redirect(reverse('cal:calendar_events_list', kwargs={'pk': cal.id}))
        else:
            if token.active:
                return render(request, self.template_name, {'object': cal})
        raise Http404("Calendar not found")

    def post(self, request, *args, **kwargs):
        t = self.kwargs.get('token')
        token = CalendarShareToken.objects.get(token=t)

        cal = token.calendar
        if request.user in cal.subscribers.all() or request.user == cal.owner:
            return redirect(reverse('cal:calendar_events_list', kwargs={'pk': cal.id}))
        else:
            if token.active:
                cal.subscribers.add(request.user)
                return redirect(reverse('cal:calendar_events_list', kwargs={'pk': cal.id}))
        raise Http404("Calendar not found")


class CalendarRemoveSubscriberView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        cal_id = self.kwargs.get('pk')
        try:
            cal = Calendar.objects.owned(request).get(pk=cal_id)
            user = User.objects.get(pk=user_id)
        except Calendar.DoesNotExist:
            raise Http404()
        except User.DoesNotExist:
            raise Http404()
        cal.subscribers.remove(user)
        print(cal.subscribers.all())
        next_url = request.POST.get('next') or None
        if next_url is not None:
            return redirect(next_url)
        return redirect(reverse('cal:calendar_detail', kwargs={'pk': cal_id}))


class CalendarAddSubscriberView(LoginRequiredMixin, View):
    template_name = 'cal/subscribers/add.html'

    def get(self, request, *args, **kwargs):
        context = {
            'object': get_object_or_404(Calendar, pk=self.kwargs.get('pk')),
            'user_list': User.objects.all()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        cal_id = self.kwargs.get('pk')
        try:
            cal = Calendar.objects.owned(request).get(pk=cal_id)
            user = User.objects.get(pk=user_id)
        except Calendar.DoesNotExist:
            raise Http404()
        except User.DoesNotExist:
            raise Http404()
        cal.subscribers.add(user)

        context = {
            'object': cal,
            'user_list': User.objects.all()
        }
        return render(request, self.template_name, context)


def handler404(request, *args, **argv):
    return render(request, 'cal/404.html', {})
# invite guests
# accept / reject invitation
