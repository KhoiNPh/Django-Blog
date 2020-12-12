from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


STATUS = (
    (0, "Draft"),
    (1, "Publish"),
    (2, "Coverphoto"),
    (3, "Blogger")
)

LANGUAGE = (
    ("English", "English"),
    ("French", "French"),
    ("Vietnamese", "Vietnamese")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    thumb = models.ImageField(default="default.png", blank=True)
    quotation = models.CharField(max_length=1200)
    language = models.CharField(
        choices=LANGUAGE, default="English", max_length=20)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey(
        'Comment', null=True, related_name="replies",  on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug


class Message(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=400, default='No subject')
    content = models.TextField()
    user_to_reply = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE, null=True,
                                      default=int(''.join(map(str, User.objects.filter(is_superuser=True).values_list('id')[0]))))
    created_on = models.DateTimeField(auto_now_add=True)
    is_replied = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.email


# class Mail(models.Model):
#     message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mails')
#     subject = models.CharField(max_length=400, default='No subject')
#     content = models.TextField()
#     created_on = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.subject
