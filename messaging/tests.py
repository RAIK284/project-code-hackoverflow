from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile

# Helper Functions
def create_profile(username: str, first_name: str, last_name: str, display_points: bool, points: int) -> Profile:
    """
    Helper function that creates a profile for a user.

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
    Helper function that gets a user's full name from a Profile Model.
    
    :param profile - Profile Model
    :return the username as a str
    """
    return User.objects.get(id=profile.user.id).get_full_name()

# View Tests
class ConversationViewTests(TestCase):
    pass

class InboxViewTests(TestCase):
    pass

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

    def test_several_users_mix(self):
        """Tests that the leaderboard only shows public profiles and orders them by points descending."""
        public1 = create_profile("public1", "Public", "One", display_points=True, points=10)
        public2 = create_profile("public2", "Public", "Two", display_points=True, points=20)
        _ = create_profile("private1", "Private", "One", display_points=False, points=30)
        
        expected_user_data = [(get_user_full_name(public2), public2.points), (get_user_full_name(public1), public1.points)]

        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(
            response.context['users'],
            expected_user_data
        )

    def test_several_users_overflow(self):
        """Tests that the leaderboard still displays a set number of profiles when a lot exist and orders them by points descending."""
        NUM_USERS_TO_SHOW = 10

        public_profiles = []
        for i in range(NUM_USERS_TO_SHOW + 3):
            public_profiles.append(create_profile(f"public{i}", "Public", f"{i}", display_points=True, points=(i * 10)))
        
        # Add the profiles to the expected data in descending order
        profiles_to_show = public_profiles[3:]
        expected_user_data = []
        for profile in profiles_to_show:
            expected_user_data.insert(0, (get_user_full_name(profile), profile.points))

        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(
            response.context['users'],
            expected_user_data
        )
