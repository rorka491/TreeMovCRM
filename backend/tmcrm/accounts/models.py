import uuid
from django.db import models
from mainapp.models import BaseModelOrg


class Invite(BaseModelOrg): 
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_used = models.BooleanField(default=False)


