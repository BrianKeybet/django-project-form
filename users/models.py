from django.db import models
from django.contrib.auth.models import User
from forms.models import Department
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    authentication = models.CharField(max_length=7, null=True, default='0')
    level = models.IntegerField(null=True, default='1')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    department = models.CharField(max_length=20, blank=False, default='Warehouse')
    # department = models.ForeignKey(Department, on_delete=models.PROTECT)
    email = models.EmailField(max_length=254, blank=False, default='support.user2@kapa-oil.local')

    def __str__(self):
        return f'{self.user.username} Profile'

#Function to grab saved image and resize it
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
