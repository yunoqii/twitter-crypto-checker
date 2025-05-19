from django.db import models

class Influencer(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username

class InfluencerFollow(models.Model):
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE, related_name='follows')
    followed_username = models.CharField(max_length=255)

    class Meta:
        unique_together = ('influencer', 'followed_username')

    def __str__(self):
        return f"{self.influencer.username} ➝ {self.followed_username}"
