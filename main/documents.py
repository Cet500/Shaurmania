from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Shaurma


@registry.register_document
class ShaurmaDocument( Document ):
	class Index:
		name = 'shaurma'
		search = { 'number_of_shards': 1, 'number_of_replicas': 0 }

	class Django:
		model = Shaurma

		fields = [
			'name',
			'description'
		]
