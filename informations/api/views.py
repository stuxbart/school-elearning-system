from rest_framework import viewsets

from ..models import News
from ..serializers import NewsSerializer

from accounts.permissions import IsAdminStaffTeacherOrReadOnly, IsAdminStaffOwnerOrReadOnly


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'create']:
            permission_classes.append(IsAdminStaffTeacherOrReadOnly)
        else:
            permission_classes.append(IsAdminStaffOwnerOrReadOnly)
        return [permission() for permission in permission_classes]
