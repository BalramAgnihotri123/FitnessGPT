from django.db import models
import uuid

# Create your models here.

class user_history(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                        unique = True,
                        primary_key= True)
    
    created = models.DateTimeField(auto_now_add=True)
    
    data = models.JSONField(default=list)

    def __str__(self):
        return str(self.id)