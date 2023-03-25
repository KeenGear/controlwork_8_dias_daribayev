from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


def upload_to(instance, filename):
    return f'uploads/user_{instance.author.id}/{filename}'


# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('Moderated', 'Moderated'),
        ('Not Moderated', 'Not Moderated')
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Moderated')
    image = models.ImageField(upload_to=upload_to, blank=True, default='/gray_pic.jpg')
    review = models.TextField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} {self.average_rating()}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def average_rating(self) -> float:
        return Rating.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def can_edit(self, user):
        return self.author == user


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text

    def can_edit(self, user):
        return self.author == user


class Rating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5)])

    def __str__(self):
        return f"{self.post.title}: {self.rating}"
