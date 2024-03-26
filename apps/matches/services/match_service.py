from django.db.models import Q
from apps.users.models import UserProfile  # Adjust the import path based on your project structure
from ..models import Match

class MatchFilteringService:
    @staticmethod
    def filter_matches_with_images(user):
        user_matches = Match.objects.filter(Q(user1=user) | Q(user2=user))
        filtered_matches = []

        for match in user_matches:
            user1_profile_exists = UserProfile.objects.filter(user=match.user1).exists()
            user2_profile_exists = UserProfile.objects.filter(user=match.user2).exists()

            if user1_profile_exists and user2_profile_exists:
                user1_profile = UserProfile.objects.get(user=match.user1)
                user2_profile = UserProfile.objects.get(user=match.user2)

                if user1_profile.images.filter(active=True).exists() and user2_profile.images.filter(active=True).exists():
                    filtered_matches.append(match)
        
        return filtered_matches