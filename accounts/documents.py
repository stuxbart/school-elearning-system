from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import User

@registry.register_document
class UserDocument(Document):
    class Index:
        name = 'users'

        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    user_index = fields.IntegerField()
    class Django:
        model = User

        fields = [
            'full_name'
        ]
