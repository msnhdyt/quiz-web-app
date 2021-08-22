from django.db import models
from topic.models import Topic

# Create your models here.

class Quizzes(models.Model):
    id = models.CharField(max_length=15, primary_key=True, unique=True)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='quiz', db_constraint=False)

    def __str__(self):
        return self.title

