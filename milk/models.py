# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

GENDER = [
('Male', 'Male'),
('Female', 'Female'),
('Other', 'Other'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, default='-')
    last_name = models.CharField(max_length=20, default='-')
    gender = models.CharField(max_length=9, choices=GENDER, default="-")
    age = models.IntegerField(blank=True, null=True)
    email_confirmed = models.BooleanField(default=False)
    dp = models.ImageField(upload_to='images/', default='images/default.jpg', null=True, blank=True)
    country = models.CharField(max_length=20, blank=True, default='-')
    twitter = models.CharField(max_length=22, blank=True, null=True, default='', help_text="Don't add '@'")
    instagram = models.CharField(max_length=22, blank=True, null=True, default=' ')
    facebook = models.CharField(max_length=22, blank=True, null=True, default=' ')
    linkedin = models.CharField(max_length=22, blank=True, null=True, default=' ')
    snapchat = models.CharField(max_length=22, blank=True, null=True, default=' ')
    tiktok = models.CharField(max_length=22, blank=True, null=True, default=' ')
    github = models.CharField(max_length=22, blank=True, null=True, default=' ')
    telegram = models.CharField(max_length=22, blank=True, null=True, default=' ')
    joined = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(max_length=230, default="Hi welcome to my profile")

    class Meta:
        ordering = ['joined']

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    creator = models.CharField(max_length=12, default='Anonymous')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    post_pic = models.ImageField(upload_to='post_pics/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=1)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('post_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=12, default='Anonymous')
    body = models.TextField()
    dp = models.ImageField(upload_to="comment_dp", null=True)
    comment_pic = models.ImageField(upload_to='comment_pics', null=True, blank=True)
    likes = models.IntegerField(default=0)
    created_on = models.TimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('comment_detail', args=[str(self.id)])


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    name = models.CharField(max_length=12, default='Anonymous')
    body = models.TextField()
    dp = models.ImageField(upload_to="comment_dp", null=True)
    likes = models.IntegerField(default=0)
