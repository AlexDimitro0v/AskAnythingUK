from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from main.models import FeedbackRequest

@registry.register_document
class FeedbackRequestDocument(Document):
    class Index:
        name = 'requests'

    class Django:
        model = FeedbackRequest
        
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}
        fields = [
            'title',
            'maintext',
        ]
