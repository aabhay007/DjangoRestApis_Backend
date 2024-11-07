from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    # damage = models.CharField(max_length=100)
    # magical_powers = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.BinaryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name