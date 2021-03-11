from django.conf import settings
from django.core.mail import send_mail
from django.template import engines, Context
from django.urls import reverse


ADDED_TO_COURSE_HTML = 'courses/email/added_to_course.html'

ADDED_TO_COURSE_TXT = 'courses/email/added_to_course.txt'

def get_absolue_path(path):
    return settings.LINK_DOMAIN + path

class EmailTemplateContext(Context):
    def __init__(self, user, dict_=None, **kwargs):
        if dict_ is None:
            dict_ = {}
        context = {
            'user': user,
            'platform_url': settings.LINK_DOMAIN
        }
        context.update(dict_)
        super().__init__(context, **kwargs)


def send_member_email(membership):
    user = membership.user
    course = membership.course
    course_link = get_absolue_path(course.get_absolute_url())
    context = EmailTemplateContext(
        user,
        {
            'course_path': course_path,
            'course': course
        }
    )
    subject = 'Added to {} course'.format(course.name)

    dt_engine = engines['django'].engine
    text_body_template = dt_engine.get_template(ADDED_TO_COURSE_TXT)
    text_body = text_body_template.render(context=context)
    html_body_template = dt_engine.get_template(ADDED_TO_COURSE_HTML)
    html_body = html_body_template.render(context=context)

    send_mail(
        subject=subject,
        message=text_body,
        from_email=settings.FROM_EMAIL,
        recipient_list=(subscriber.email,),
        html_message=html_body
    )