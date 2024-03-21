# apps/matches/services/matchmaking_service.py
from apps.users.models import UserPreferences, UserProfile, Image
from ..models import CompatibilityScore, Swipe
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from utils.media_util import build_absolute_image_url
import random

class MatchmakingService:
    @staticmethod
    def get_random_data(field):
        # Expanded sample data for each field, tripled in size
        sample_data = {
            'first_name': ['Alex', 'Jamie', 'Chris', 'Pat', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Drew', 'Jesse', 'Quinn', 'Reese', 'Riley', 'Sawyer', 'Sydney'],
            'last_name': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris'],
            # Make sure other keys match your model fields
            'interests': [
                'reading, traveling', 'hiking, coding', 'photography, music', 'gaming, sports',
                'cooking, baking', 'gardening, yoga', 'swimming, dancing', 'writing, drawing',
                'fishing, camping', 'cycling, running', 'volunteering, DIY', 'singing, playing instruments',
                'board games, puzzles', 'collecting, crafting', 'astronomy, chess'
            ],
            'goals': [
                'learn a new language', 'travel more', 'pick up a new hobby', 'advance my career',
                'get fit', 'write a book', 'start a business', 'learn to cook', 'buy a house',
                'complete a marathon', 'take up meditation', 'improve financial health', 'build a personal brand',
                'develop a new skill', 'make new friends'
            ],
            'zodiac_sign': ['Gemini', 'Libra', 'Aries', 'Taurus', 'Leo', 'Virgo', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces', 'Cancer'],
            'biography': [
                'Loves adventure and meeting new people.', 'Tech enthusiast and nature explorer.', 'Avid reader and aspiring writer.',
                'Passionate about fitness and health.', 'Creative soul with a love for art and music.', 'Entrepreneur at heart with a knack for innovation.',
                'Globetrotter with a quest for cultural experiences.', 'Foodie who loves experimenting with new recipes.',
                'Eco-conscious and committed to making a difference.', 'Fitness junkie dedicated to a healthy lifestyle.',
                'Tech-savvy and always on the lookout for new trends.', 'Bookworm with a passion for history and literature.'
            ],
            'age': list(range(18, 51)),
            'location': [
                'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 
                'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte'
            ],
            'education': [
                'High School diploma', 'Bachelor\'s Degree', 'Master\'s Degree', 'Ph.D.', 'Associate Degree',
                'Trade School Certificate', 'No formal education', 'Some college, no degree', 'Professional degree',
                'Educational specialist', 'Senior Secondary Certificate', 'Vocational qualification', 'GED', 'International Baccalaureate', 'Others'
            ],
            'hobbies': [
                'Reading', 'Traveling', 'Hiking', 'Coding', 'Photography', 'Music', 'Sports', 'Cooking',
                'Baking', 'Gardening', 'Yoga', 'Swimming', 'Dancing', 'Writing', 'Drawing'
            ],
            'occupation': [
                'Software Developer', 'Teacher', 'Designer', 'Engineer', 'Doctor', 'Nurse', 'Architect', 'Farmer',
                'Chef', 'Electrician', 'Mechanic', 'Lawyer', 'Accountant', 'Salesperson', 'Writer'
            ],
            'relationship_status': ['Single', 'In a relationship', 'Married', 'It\'s complicated', 'Open for options'],
            'height': ['5\'4"', '5\'7"', '5\'10"', '6\'0"', '6\'3"', '5\'5"', '5\'8"', '5\'11"', '6\'1"', '6\'4"'],
            'looking_for': ['Friendship', 'A serious relationship', 'Casual dating', 'Networking', 'Nothing specific']
        }
        
        if field not in sample_data:
            # For these fields, select a random subset
            items = random.choice(sample_data[field]).split(', ')
            random.shuffle(items)
            return ', '.join(random.sample(items, random.randint(1, len(items))))
        else:
            # For other fields, return a single random value
            return random.choice(sample_data[field])

    @staticmethod
    def update_profile_with_random_data(profile):
        fields_to_check = [
            'first_name', 'last_name', 'interests', 'goals', 'zodiac_sign', 'biography',
            'age', 'location', 'education', 'hobbies', 'occupation', 'relationship_status', 'height', 'looking_for'
        ]
        update_fields = []
        for field in fields_to_check:
            # Retrieve the current value of the field
            current_value = getattr(profile, field, None)
            
            # Check if the value is None or "Not specified"
            if current_value is None or current_value == "Not specified":
                # Generate and set random data for the field
                random_data = MatchmakingService.get_random_data(field)
                setattr(profile, field, random_data)  # Correct use of setattr to update the model instance
                update_fields.append(field)

        # Save the profile with updated fields, if any
        if update_fields:
            profile.save(update_fields=update_fields)

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
            MatchmakingService.update_profile_with_random_data(match)  # Update profile with random data if necessary
            
            # Initialize an empty list for images
            images_list = []
            
            # Fetch images associated with the user profile
            images = Image.objects.filter(user_profile=match)
            for image in images:
                try:
                    # Generate the absolute URL for the image
                    # image_url = build_absolute_image_url(request, image.image);
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
                    'id': match.user.id,
                    'firstName': match.first_name,
                    'lastName': match.last_name,
                    'interests': match.interests,
                    'goals': match.goals,
                    'zodiacSign': match.zodiac_sign,
                    'username': match.user.username,
                    'biography': match.biography,
                    'age': match.age,
                    'location': match.location,
                    'images': images_list,
                    'education': match.education,
                    'hobbies': match.hobbies,
                    'occupation': match.occupation,
                    'relationshipStatus': match.relationship_status,
                    'height': match.height,
                    'lookingFor': match.looking_for,
                    'isVerified': True,  # Assuming all users are verified for simplicity
                }
                match_data.append(match_dict)

        return match_data
    
# Assuming this is placed in a utilities module or directly within your serializer file
def get_random_user_image_url(user):
    images = Image.objects.filter(user_profile=user.profile)  # Adjust based on your actual relationship
    if images.exists():
        # Select a random image if multiple images are present
        random_image = random.choice(images)
        return random_image.image.url  # Assuming 'image' is the ImageField
    return None