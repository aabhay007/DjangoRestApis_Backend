from django.db import models


# region items
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.BinaryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    # endregion

#region task
class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    email = models.EmailField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
#endregion