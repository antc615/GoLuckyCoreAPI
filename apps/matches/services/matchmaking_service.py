# apps/matches/services/matchmaking_service.py

from apps.users.models import UserPreferences, UserProfile
from ..models import CompatibilityScore, Swipe
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

class MatchmakingService:
    @staticmethod
    def get_recommendations(user):
        try:
            user_prefs = UserPreferences.objects.get(user=user)
        except ObjectDoesNotExist:
            # Handle case where user preferences are not set
            return {"error": "User preferences not set."}

        potential_matches = UserProfile.objects
        # .exclude(user=user).filter(
        #     age__gte=user_prefs.age_range_min,
        #     age__lte=user_prefs.age_range_max,
        #     # Add more filters based on user_prefs
        # )
        
        # Further refine matches based on compatibility scores
        # refined_matches = potential_matches.filter(
        #     Q(user__compatibility_scores_as_user1__user2=user) |
        #     Q(user__compatibility_scores_as_user2__user1=user)
        # ).order_by('-user__compatibility_scores_as_user1__score', '-user__compatibility_scores_as_user2__score')

        # Exclude users already swiped left or blocked
        # swiped_users = Swipe.objects.filter(swiper=user, direction='dislike').values_list('swiped', flat=True)
        
        # Safely process blocked user IDs
        blocked_user_ids = []
        for user_id_str in user_prefs.block_list.split(','):
            user_id_str = user_id_str.strip()
            if user_id_str:  # Check if the string is not empty
                try:
                    user_id = int(user_id_str)
                    blocked_user_ids.append(user_id)
                except ValueError:
                    # Skip invalid entries
                    continue

        # final_recommendations = refined_matches.exclude(user__in=swiped_users).exclude(user__in=blocked_user_ids)
        
        if not potential_matches.exists():
            # Handle case where no potential matches are found
            return {"error": "No potential matches found."}

        # return list(potential_matches.values('user__username', 'biography', 'age', 'location'))
        return list(potential_matches.values)
        
        # if not final_recommendations.exists():
        #     # Handle case where no potential matches are found
        #     return {"error": "No potential matches found."}

        # return list(final_recommendations.values('user__username', 'biography', 'age', 'location'))
