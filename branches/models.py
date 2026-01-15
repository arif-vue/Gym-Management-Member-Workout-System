from django.db import models


class GymBranch(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Gym Branches'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
