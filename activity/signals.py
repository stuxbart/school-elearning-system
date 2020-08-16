from django.dispatch import Signal

course_viewed_signal = Signal(providing_args=['instance', 'request'])