# School Elearning System
This platform can be used by school and enable teachers to create courses with content for students.

Project is not ended up and is not ready for production.
## Setup Project
To setup project you need to install all dependences from `requirements.txt` file in your environment:
```
pip install -r requirements.txt
```
Then you should change `SECRET_KEY` in `settings.py` file for security purposes.

Next you have to set up database, project by default uses PostgreSQL. To fast set up database you can use code below:
```sql
CREATE DATABASE school;
CREATE USER school;
ALTER USER school PASSWORD "school";
GRANT ALL ON DATABASE school TO school;
ALTER USER school CREATEDB;
```
If you have diffrent db configuration change also `DATABASES` config variable in `settings.py` file.

To apply all migrations you have to:
1. Comment out particular apps in `INSTALLED_APPS` in `settings.py` file like below:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'accounts',
    # 'courses',
    # 'activity',
    # 'search',
    # 'information',
    # 'cal',
    # 'gradebook',
    'rest_framework',
    # 'knox',
    'corsheaders',
    'django_elasticsearch_dsl',
    'crispy_forms',
    'django_celery_results',
]
```
and comment out 63 line in `settings.py` file:
```python
# AUTH_USER_MODEL = 'accounts.User'
```
When you comment out above apps you have to get rid of imports from this apps.

At first comment out whole `elearning/views.py` file, then comment out most url patterns in 
elearning/urls.py (`path('admin/', admin.site.urls)` may be uncommented), urlpatterns list
itself should not be commented.
```python
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# from .views import home_view

# api_urlpatterns = [
#     path('courses/', include('courses.api.urls.course')),
#     path('modules/', include('courses.api.urls.module')),
#     path('categories/', include('courses.api.urls.category')),
#     path('content/', include('courses.api.urls.content')),
#     path('users/', include('accounts.api.urls.users', 'users')),
#     path('auth/', include('accounts.api.urls.auth')),
#     path('news/', include('information.api.urls'))
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home_view, name='home'),
    # path('accounts/', include('accounts.urls', 'accounts')),
    # path('courses/', include('courses.urls', 'courses')),
    # path('search/', include('search.urls', 'search')),
    # path('information/', include('information.urls', 'information')),
    # path('calendar/', include('cal.urls', 'cal')),
    # path('gradebook/', include('gradebook.urls')),

    # path('api/', include((api_urlpatterns, 'api')))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
2. Now we can run migrations with:
```
python manage.py migrate
```
3. Next step is to reset migrations in admin app (knox and accounts apps need this to apply migrations):
```
python manage.py migrate admin zero
```
4. Now you can uncomment all previusly commented lines and then apply rest migrations:
```
python manage.py migrate
```
Now database is setup correctly


Next you need working Elasticsearch at `localhost:9200`, you can change this url in `settings.py` file.
Then create Elasticsearch index with:
```
manage.py search_index --rebuild
```

To setup celery you need Redis available at `redis://localhost:6379/0`, it is used as celery broker.
And then you can run:
```
celery -A elearning.celery worker -l info
```
to run celery. Celery is used only for sending emails.

Last thing that you have to do is change smtp server configuration in `settings.py` file.

You also need to create an admin account with:
``` 
python manage.py createsuperuser
```
because users can be added only by admins of this site.

Now you can run development server with:
```
python manage.py runserver
```
and go to `localhost:8000`. This page may looks empty because database is empty.