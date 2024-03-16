import uuid

from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel


class BaseModel(DjangoCassandraModel, SafeDeleteModel):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    created_at = columns.DateTime()

    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta:
        abstract = True
