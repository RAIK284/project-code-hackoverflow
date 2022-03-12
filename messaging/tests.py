from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile

# Model Tests
class ConversationModelTests(TestCase):
    pass

class MessageModelTests(TestCase):
    pass

class ProfileModelTests(TestCase):
    pass

# View Tests
class InboxViewTests(TestCase):
    pass

def create_profile(username: str, first_name: str, last_name: str, display_points: bool, points: int) -> Profile:
    """
    Creates a profile for a user.

    :param username - the username to use
    :param first_name - user's first name
    :param last_name - user's last name
    :param display_points - whether or not the profile's points are public
    :param points - the number of points for the user
    :return the created Profile
    """
    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password='12345')
    return Profile.objects.create(user=user, displayPoints=display_points, points=points)

def get_user_full_name(profile: Profile) -> str:
    """
    Gets a user's full name from a Profile Model.
    
    :param profile - Profile Model
    :return the username as a str
    """
    return User.objects.get(id=profile.user.id).get_full_name()

class LeaderboardViewTests(TestCase):
    def test_no_users(self):
        """Tests that the leaderboard displays no profiles when none exist."""
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['users'], [])

    def test_one_user_private(self):
        """Tests that the leaderboard displays no profiles when one has private data."""
        _ = create_profile("jsmith", "John", "Smith", display_points=False, points=10)
        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(response.context['users'], [])
    
    def test_one_user_public(self):
        """Tests that the leaderboard displays the sole profile with public data."""
        profile = create_profile("jsmith", "John", "Smith", True, 10)
        user_full_name = get_user_full_name(profile)
        expected_user_data = [(user_full_name, profile.points)]

        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(
            response.context['users'],
            expected_user_data
        )
