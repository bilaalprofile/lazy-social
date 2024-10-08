from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(blank=True, null=True, upload_to="profiles/")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.CharField(max_length=50)
    gender = models.CharField(max_length=30)
    country = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="posts/")
    group = models.ForeignKey(
        'SocialGroup', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_liked_by_user(self, user):
        return self.likes.filter(user=user).exists()

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    def __str__(self):
        return self.user.username + ' - ' + self.body


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes',
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user} likes {self.post}"


class Comment(DateTimeModel):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='comments/')

    def __str__(self):
        return self.post.user.username


class SocialGroup(DateTimeModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_by")
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True,
                              upload_to="group_profiles")
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name="members")

    def __str__(self):
        return self.name


class FriendRequest(DateTimeModel):
    senders = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender")
    recievers = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reciever")
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reciever.username} {str(self.accepted)}"
