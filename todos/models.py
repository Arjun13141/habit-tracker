from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def mark_complete(self):
        """Mark todo as complete"""
        self.completed = True
        self.completed_at = timezone.now()
        self.save()
    
    def mark_incomplete(self):
        """Mark todo as incomplete"""
        self.completed = False
        self.completed_at = None
        self.save()
    
    class Meta:
        ordering = ['-created_at']