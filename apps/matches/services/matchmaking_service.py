# apps/matches/services/matchmaking_service.py
from apps.users.models import UserPreferences, UserProfile, Image
from ..models import CompatibilityScore, Swipe
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from utils.media_util import build_absolute_image_url

class MatchmakingService:
    @staticmethod
    def get_recommendations(user, request):
        try:
            user_prefs, created = UserPreferences.objects.get_or_create(user=user)
        except ObjectDoesNotExist:
            # Handle case where user preferences are not set
            return {"error": "User preferences not set."}

        potential_matches = UserProfile.objects.all()
       
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

        potential_matches = potential_matches.exclude(user__in=blocked_user_ids)

        if not potential_matches.exists():
            # Handle case where no potential matches are found
            return {"error": "No potential matches found."}

        # Fetch images for potential matches
        match_data = []
        for match in potential_matches:
            # Initialize an empty list for images
            images_list = []
            
            # Fetch images associated with the user profile
            images = Image.objects.filter(user_profile=match)
            for image in images:
                try:
                    # Generate the absolute URL for the image
                    image_url = request.build_absolute_uri(image.image.url)
                    
                    # Create a dictionary with the image's URL and additional metadata
                    image_data = {
                        'url': image_url,
                        'is_profile_image': image.is_profile_picture,
                        'description': image.description
                    }
                    
                    # Append the dictionary to the images list
                    images_list.append(image_data)
                except ValueError:
                    # Skip images that cannot be accessed
                    continue

            # Only include the match if there are images
            if images_list:
                match_dict = {
                    'username': match.user.username,
                    'biography': match.biography,
                    'age': match.age,
                    'location': match.location,
                    'images': images_list,
                    'isVerified': True
                }
                # Add the match to the match data list
                match_data.append(match_dict)

        return match_data
    
