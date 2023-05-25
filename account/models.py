from django.db import models

class Name(models.Model):
    """A name model."""
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name