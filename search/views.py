from django.shortcuts import render
from django.views.generic import ListView
from courses.models import Course
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity,TrigramDistance


class MainSearchView(ListView):
    template_name = 'search/search_results.html'
    queryset = Course.objects.all()

    def get_queryset(self, *args, **kwargs):
        q = self.request.GET.get('q')
        return Course.objects.annotate(
            search=SearchVector('title', weight='A') + SearchVector('overview', weight='B')
        ).filter(search=SearchQuery(q, search_type='phrase'))
        # return Course.objects.annotate(
        #             similarity=TrigramSimilarity('title', 'siemanko'),
        #         ).filter(similarity__gt=0.3).order_by('-similarity')

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        return super().get(request, *args, **kwargs)