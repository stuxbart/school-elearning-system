from .signals import course_viewed_signal

class CourseViewedMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(CourseViewedMixin, self).get_context_data(*args, **kwargs)
        request = self.request
        course = context['object']
        if course:
            course_viewed_signal.send(course.__class__, course=course, request=request)

        return context