from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from .forms import ProfileCreateForm
from .models import Conversation, Message, Profile, UserGroup

# Helper Functions
def create_convo(convo_name: str, profiles: list[Profile]) -> Conversation:
    """
    Helper function that creates a conversation between users.

    :param convo_name - the name to give the conversation
    :param profiles - a list of profiles to extract user data from
    :return a new Conversation object
    """
    user_group = UserGroup.objects.create(name=convo_name)
    for profile in profiles:
        user = User.objects.get(id=profile.user.id)
        user_group.members.add(user)

    return Conversation.objects.create(name=convo_name, userGroup=user_group)

def create_message(sender: Profile, convo: Conversation, body: str) -> Message:
    """
    Helper function to make a message for a conversation.

    :param sender - the profile that sent the message
    :param convo - the conversation to attach the message to
    :param body - the actual message contents
    :return the message object
    """
    return Message.objects.create(sender=sender.user, conversation=convo, body=body)

def create_profile(username: str, first_name: str, last_name: str, display_points: bool, points: int=0, all_time_points: int=0, display_purchases: bool=False, password: str='YuR46aeZR', email: str='user@email.com') -> Profile:
    """
    Helper function that creates a profile for a user.

    :param username - the username to use
    :param first_name - user's first name
    :param last_name - user's last name
    :param display_points - whether or not the profile's points are public
    :param points - the number of points for the user
    :param all_time_points - the number of all time points for the user
    :param display_purchases - (optional) whether or not the profile's purchases are public
    :param password - (optional) the user's password
    :return the created Profile
    """
    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    return Profile.objects.create(user=user, displayPoints=display_points, points=points, allTimePoints=all_time_points, displayPurchases=display_purchases) 

def get_user_full_name(profile: Profile) -> str:
    """
    Helper function that gets a user's full name from a Profile Model.
    
    :param profile - Profile Model
    :return the username as a str
    """
    return User.objects.get(id=profile.user.id).get_full_name()

# Form Tests
class ProfileCreateFormTests(TestCase):
    def test_profile_create_form_all_valid_fields(self):
        """Tests that the profile create form can be filled properly."""
        # Note: username, password1, and password2 all extra required for User creation
        form_data = {
            'username': 'lknope',
            'password1': 'YuR46aeZR',
            'password2': 'YuR46aeZR',
            'first_name': 'Leslie',
            'last_name': 'Knope',
            'email': 'lknope@pawnee.com'
        }

        form = ProfileCreateForm(data=form_data)
        self.assertTrue(form.is_valid(), msg="Expected the form to be valid if all the fields are valid, but failed.")

    def test_profile_create_form_valid_save_user(self):
        """Tests that the profile create form can be filled properly and save a new user correctly."""
        # Note: username, password1, and password2 all extra required for User creation
        form_data = {
            'username': 'lknope',
            'password1': 'YuR46aeZR',
            'password2': 'YuR46aeZR',
            'first_name': 'Leslie',
            'last_name': 'Knope',
            'email': 'lknope@pawnee.com'
        }

        form = ProfileCreateForm(data=form_data)
        actual_user, _ = form.save(commit=False)
        user_correct = \
            actual_user.username == form_data['username'] and \
            actual_user.first_name == form_data['first_name'] and \
            actual_user.last_name == form_data['last_name'] and \
            actual_user.email == form_data['email']

        self.assertTrue(user_correct, msg="Expected the right user to be made if all the fields are valid, but failed.")

    def test_profile_create_form_invalid_empty_fields(self):
        """Tests that the form is invalid with empty fields."""
        form = ProfileCreateForm(data={})
        self.assertFalse(form.is_valid(), msg="Expected the form to be invalid with no data, but it was marked valid.")

    def test_profile_create_form_invalid_missing_fields(self):
        """Tests that the form is invalid with missing fields."""
        form_data = {
            'username': 'lknope',
            'password1': 'YuR46aeZR',
            'password2': 'YuR46aeZR',
            'first_name': 'Leslie',
        }

        form = ProfileCreateForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="Expected the form to be invalid with missing data, but it was marked valid.")

class ProfileUpdateFormTests(TestCase):
    pass

# Model Tests
class ProfileModelTests(TestCase):
    def test_profile_remind_user_no_messages(self):
        """Tests that a user will get an email if they have never sent a message."""
        prof = create_profile('jgeng', 'Jerry', 'Gengert', False, 0)
        actual_response = prof.remind_user_to_send_message()
        self.assertEquals(1, actual_response, f"Expected one email to be sent to a user with no messages, but {actual_response} was/were sent.")
    
    def test_profile_remind_user_not_sent_recent(self):
        """Tests that a user will get an email if they haven't sent a message recently (last 2 days)."""
        DAYS_TO_CHECK = 2
        sender = create_profile('rswanson', 'Ron', 'Swanson', False, 0)
        receiver = create_profile('aperkins', 'Anne', 'Perkins', True, 0, display_purchases=True)

        # Freeze time so that the message occurs in the past
        convo = create_convo("Positive Conversation.", [sender, receiver])
        with freeze_time(timezone.now() - timedelta(DAYS_TO_CHECK + 1)):
            _ = create_message(sender, convo, "This is a positive message. Hello.")

        actual_response = sender.remind_user_to_send_message()
        self.assertEquals(1, actual_response, f"Expected one email to be sent to a user with no recent messages, but {actual_response} was/were sent.")

    def test_profile_remind_user_sent_recent(self):
        """Tests that a user won't get an email if they sent a message recently (last 2 days)."""
        sender = create_profile('rswanson', 'Ron', 'Swanson', False, 0)
        receiver = create_profile('tomh', 'Tom', 'Haverford', True, 0, display_purchases=True)
        convo = create_convo("Positive Conversation.", [sender, receiver])
        _ = create_message(sender, convo, "This is a positive message. Hello.")

        actual_response = sender.remind_user_to_send_message()
        self.assertEquals(0, actual_response, f"Expected no email to be sent to a user with a recent message, but {actual_response} was/were sent.")

# View Tests
class ConversationViewTests(TestCase):
    def test_convo_one_message_convo_returned(self):
        """Tests that a conversation is returned when it has one message."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
        convo = create_convo("mscott-dschrute", [profile1, profile2])
        _ = create_message(profile1, convo, "Hi Dwight!")

        self.client.force_login(profile1.user)

        response = self.client.get(reverse('conversation', args=[convo.id]))
        self.assertEquals(
            response.context['convo'],
            convo,
            msg=f"Expected a conversation with name {convo.name} to be returned when {profile1.user.username} is logged in, but failed."
        )

    def test_convo_one_message_msg_returned(self):
        """Tests that the right message is returned from a conversation with one message."""
        profile1 = create_profile("mscott", "Michael", "Scott", True)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False)
        convo = create_convo("mscott-dschrute", [profile1, profile2])
        expected_msg = create_message(profile1, convo, "Hi Dwight!")

        self.client.force_login(profile1.user)

        response = self.client.get(reverse('conversation', args=[convo.id]))
        self.assertQuerysetEqual(
            response.context['messages'],
            [expected_msg],
            msg=f"Expected the message in a conversation with name {convo.name} to be returned when {profile1.user.username} is logged in, but failed."
        )

    def test_convo_one_message_name_returned(self):
        """Tests that the right first name is returned from a conversation with one message."""
        profile1 = create_profile("mscott", "Michael", "Scott", True)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False)
        convo = create_convo("mscott-dschrute", [profile1, profile2])
        _ = create_message(profile1, convo, "Hi Dwight!")

        self.client.force_login(profile1.user)

        response = self.client.get(reverse('conversation', args=[convo.id]))
        self.assertEquals(
            response.context['first_name'],
            profile1.user.first_name,
            msg=f"Expected the sender's first name in a conversation with name {convo.name} to be returned when {profile1.user.username} is logged in, but failed."
        )

    def test_convo_one_message_members_returned(self):
        """Tests that the members are returned from a conversation with one message."""
        profile1 = create_profile("mscott", "Michael", "Scott", True)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False)
        convo = create_convo("mscott-dschrute", [profile1, profile2])
        _ = create_message(profile1, convo, "Hi Dwight!")

        self.client.force_login(profile1.user)

        response = self.client.get(reverse('conversation', args=[convo.id]))
        self.assertQuerysetEqual(
            response.context['members'],
            [profile2.user, profile1.user],
            msg=f"Expected the members in a conversation with name {convo.name} to be returned when {profile1.user.username} is logged in, but failed."
        )

    def test_convo_several_messages_msgs_returned(self):
        """Tests that the right messages are returned from a conversation with multiple messages."""
        profile1 = create_profile("mscott", "Michael", "Scott", True)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False)
        convo = create_convo("mscott-dschrute", [profile1, profile2])
        expected_msg1 = create_message(profile1, convo, "Hi Dwight!")
        expected_msg2 = create_message(profile2, convo, "Hello Michael.")

        self.client.force_login(profile1.user)

        response = self.client.get(reverse('conversation', args=[convo.id]))
        self.assertQuerysetEqual(
            response.context['messages'],
            [expected_msg1, expected_msg2],
            msg=f"Expected the messages in a conversation with name {convo.name} to be returned when {profile1.user.username} is logged in, but failed."
        )

    def test_convo_two_users_send_points_receives_properly(self):
        """Tests that a user can send points to another user."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, points=30)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False)
        convo = create_convo("mscott-dschrute", [profile1, profile2])

        data = {
            'body': "Hi Dwight! 🐶 xoxoxo"
        }

        # Post the message, which sends the points
        self.client.force_login(profile1.user)
        _ = self.client.post(reverse('conversation', args=[convo.id]), data)
        profile2.refresh_from_db()

        expected_points = 10
        self.assertEqual(profile2.allTimePoints, expected_points,
        f"Expected sending a token in a message to give {expected_points} points, but the recipient has {profile2.allTimePoints} instead.")

    def test_convo_two_users_send_points_subtracts_properly(self):
        """Tests that a user's points is deducted when they send to another user."""
        pass

    def test_convo_two_users_send_points_not_enough(self):
        """Tests that a user can't send points to another user if they don't have enough."""
        pass

    def test_convo_three_users_points_spread_equally(self):
        """Tests that two users receive half the total amount of points that should be sent."""
        pass

class InboxViewTests(TestCase):
    def test_inbox_no_display_no_convos(self):
        """Tests that no conversations are rendered when none exist for a user."""
        prof = create_profile("mscott", "Michael", "Scott", True, 0)

        self.client.force_login(prof.user)

        response = self.client.get(reverse('inbox'))
        self.assertEquals(
            response.context['names'],
            [],
            msg=f"Expected no conversations to be returned when logged in but none exist, but failed."
        )

    def test_inbox_no_display_not_logged_in(self):
        """Tests that no conversations are rendered when a user isn't logged in."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
        _ = create_convo("mscott-dschrute", [profile1, profile2])

        response = self.client.get(reverse('inbox'))
        self.assertIsNone(
            response.context,
            msg=f"Expected no conversation to be returned when not logged in, but failed."
        )

    def test_inbox_one_convo_two_users(self):
        """Tests that a conversation between two users is shown when one user is logged in."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
        convo = create_convo("mscott-dschrute", [profile1, profile2])

        self.client.force_login(profile1.user)

        response = self.client.get(reverse('inbox'))
        self.assertEquals(
            response.context['names'][0][0].name,
            convo.name,
            msg=f"Expected a conversation with name {convo.name} to be returned when {profile1.user.username} is logged in, but failed."
        )

    def test_inbox_one_convo_two_users_other_logged_in(self):
        """Tests that a conversation between two users is shown when the other user is logged in."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
        convo = create_convo("mscott-dschrute", [profile1, profile2])

        self.client.force_login(profile2.user)

        response = self.client.get(reverse('inbox'))
        self.assertEquals(
            response.context['names'][0][0].name,
            convo.name,
            msg=f"Expected a conversation with name {convo.name} to be returned when {profile2.user.username} is logged in, but failed."
        )

    def test_inbox_multiple_convos(self):
        """Tests that three conversations are shown in order of most recent to least recent when the user is logged in."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
        profile3 = create_profile("jhalpert", "Jim", "Halpert", True, 100)
        profile4 = create_profile("pbeasly", "Pam", "Beasly", True, 200)

        _ = create_convo("mscott-dschrute", [profile1, profile2])
        _ = create_convo("mscott-jhalpert", [profile1, profile3])
        _ = create_convo("mscott-pbeasly", [profile1, profile4])

        self.client.force_login(profile1.user)

        response = self.client.get(reverse('inbox'))
        self.assertEquals(
            len(response.context['names']),
            3,
            msg=f"Expected three conversations to be returned when {profile1.user.username} is logged in, but failed."
        )

class LeaderboardViewTests(TestCase):
    def test_leaderboard_no_users(self):
        """Tests that the leaderboard displays no profiles when none exist."""
        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(response.context['user_data'], [], msg="Leaderboard displays profiles when none were expected.")

    def test_leaderboard_one_user_private(self):
        """Tests that the leaderboard displays no profiles when one has private data."""
        _ = create_profile("jsmith", "John", "Smith", display_points=False)

        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(response.context['user_data'], [], msg=f"Leaderboard displayed {response.context['user_data']}, when no public users were expected.")
    
    def test_leaderboard_one_user_public(self):
        """Tests that the leaderboard displays the sole profile with public data."""
        profile = create_profile("jsmith", "John", "Smith", True)
        expected_user_data = [(profile.user, profile.allTimePoints)]

        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(
            response.context['user_data'],
            expected_user_data,
            msg=f"Leaderboard displayed {response.context['user_data']}, when only one public user was expected: {expected_user_data}."
        )

    def test_leaderboard_several_users_mix(self):
        """Tests that the leaderboard only shows public profiles and orders them by points descending."""
        public1 = create_profile("public1", "Public", "One", display_points=True, all_time_points=10)
        public2 = create_profile("public2", "Public", "Two", display_points=True, all_time_points=30)
        _ = create_profile("private1", "Private", "One", display_points=False, all_time_points=20)
        
        expected_user_data = [(public2.user, public2.allTimePoints), (public1.user, public1.allTimePoints)]

        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(
            response.context['user_data'],
            expected_user_data,
            msg=f"Leaderboard displayed {response.context['user_data']}, when only the public profiles {expected_user_data} were expected."
        )

    def test_leaderboard_several_users_overflow(self):
        """Tests that the leaderboard still displays a set number of profiles when a lot exist and orders them by points descending."""
        NUM_USERS_TO_SHOW = 10

        public_profiles = []
        for i in range(NUM_USERS_TO_SHOW + 3):
            new_profile = create_profile(f"public{i}", "Public", f"{i}", display_points=True, all_time_points=(i*10))
            public_profiles.append(new_profile)
        
        # Add the profiles to the expected data in descending order
        profiles_to_show = public_profiles[3:]
        expected_user_data = []
        for profile in profiles_to_show:
            expected_user_data.insert(0, (profile.user, profile.allTimePoints))

        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(
            response.context['user_data'],
            expected_user_data,
            msg=f"Leaderboard did not display the 10 expected users."
        )
