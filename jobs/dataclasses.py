import uuid

from commons.dataclasses import BaseDataClass


class CreateJobDataClass(BaseDataClass):
    id: uuid.UUID
