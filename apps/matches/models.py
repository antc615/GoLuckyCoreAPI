from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Match(models.Model):
    user1 = models.ForeignKey(User, related_name='matches_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='matches_as_user2', on_delete=models.CASCADE)
    matched_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1.username} and {self.user2.username}"

class Swipe(models.Model):
    SWIPE_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )

    swiper = models.ForeignKey(User, related_name='swipes_made', on_delete=models.CASCADE)
    swiped = models.ForeignKey(User, related_name='swipes_received', on_delete=models.CASCADE)
    direction = models.CharField(max_length=10, choices=SWIPE_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    reaction = models.TextField(blank=True, null=True)
    context = models.JSONField(blank=True, null=True)

    class Meta:
        unique_together = ('swiper', 'swiped')

    def __str__(self):
        return f"{self.swiper.username} swiped {self.direction} on {self.swiped.username}"

class Favorites(models.Model):
    user = models.ForeignKey(User, related_name='favorite_setter', on_delete=models.CASCADE)
    favorite = models.ForeignKey(User, related_name='favorite_target', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'favorite')

    def __str__(self):
        return f"{self.user.username} favorited {self.favorite.username}"

class MatchFeedback(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_feedbacks')
    feedback = models.TextField()
    rating = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on match {self.match.id}"

class CompatibilityScore(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compatibility_scores_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compatibility_scores_as_user2')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    calculated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compatibility Score between {self.user1.username} and {self.user2.username}: {self.score}"

class MatchRecommendation(models.Model):
    recommender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations_made')
    recommended_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations_received')
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.recommender_user.username} to match with {self.recommended_user.username}"
