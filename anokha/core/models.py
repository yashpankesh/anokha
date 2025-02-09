from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/images/', blank=True, null=True)  # For category image
    video = models.FileField(upload_to='categories/videos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=50)  # e.g., "New", "Vintage"
    brand = models.CharField(max_length=100)
    year_of_manufacture = models.IntegerField()
    image = models.ImageField(upload_to='items/',blank=True, null=True)
    stock = models.IntegerField(default=0)
    owner_name = models.CharField(max_length=200,blank=True,null=True)
    owner_phone_number = models.CharField(max_length=15, blank=True, null=True)
    owner_email = models.EmailField(max_length=200,blank=True,null=True)
    owner_address = models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.name
    
    def has_image(self):
        """Check if the item has an associated image."""
        return bool(self.image and hasattr(self.image, 'url'))

class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1)
    review_text = models.TextField()

    def __str__(self):
        return f"Review for {self.item.name}"
    
    
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField() 
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

class meta:
    ordering = ['-published_date']
