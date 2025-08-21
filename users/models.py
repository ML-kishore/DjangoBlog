from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
from PIL import Image
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # one user will have one profile picture
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self, *args, **kwargs):   # ✅ accept args & kwargs
        super().save(*args, **kwargs)  # ✅ pass them to parent save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
