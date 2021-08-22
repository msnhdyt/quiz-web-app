from django.db import models

# Create your models here.
class Topic(models.Model):
    code = models.CharField(primary_key=True, max_length=10, unique=True)
    title = models.CharField(max_length=50, null=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.title