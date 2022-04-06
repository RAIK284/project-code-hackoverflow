from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from messaging.views import conversation, profile

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

def create_profile(username: str, first_name: str, last_name: str, display_points: bool, points: int, display_purchases: bool=False, password: str='YuR46aeZR', email: str='user@email.com') -> Profile:
    """
    Helper function that creates a profile for a user.

    :param username - the username to use
    :param first_name - user's first name
    :param last_name - user's last name
    :param display_points - whether or not the profile's points are public
    :param points - the number of points for the user
    :param display_purchases - (optional) whether or not the profile's purchases are public
    :param password - (optional) the user's password
    :return the created Profile
    """
    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    return Profile.objects.create(user=user, displayPoints=display_points, points=points, displayPurchases=display_purchases) 

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
            'email': 'lknope@pawnee.com',
            'bio': 'Head of Pawnee Parks & Rec!',
            'make_my_points_public': True,
            'make_my_purchases_public': True
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
            'email': 'lknope@pawnee.com',
            'bio': 'Head of Pawnee Parks & Rec!',
            'make_my_points_public': True,
            'make_my_purchases_public': True
        }

        form = ProfileCreateForm(data=form_data)
        actual_user, _ = form.save(commit=False)
        user_correct = \
            actual_user.username == form_data['username'] and \
            actual_user.first_name == form_data['first_name'] and \
            actual_user.last_name == form_data['last_name'] and \
            actual_user.email == form_data['email']

        self.assertTrue(user_correct, msg="Expected the right user to be made if all the fields are valid, but failed.")

    def test_profile_create_form_valid_save_profile(self):
        """Tests that the profile create form can be filled properly and save a new profile correctly."""
        # Note: username, password1, and password2 all extra required for User creation
        form_data = {
            'username': 'lknope',
            'password1': 'YuR46aeZR',
            'password2': 'YuR46aeZR',
            'first_name': 'Leslie',
            'last_name': 'Knope',
            'email': 'lknope@pawnee.com',
            'bio': 'Head of Pawnee Parks & Rec!',
            'make_my_points_public': True,
            'make_my_purchases_public': True
        }

        form = ProfileCreateForm(data=form_data)
        _, actual_profile = form.save(commit=False)
        profile_correct = \
            actual_profile.bio == form_data['bio'] and \
            actual_profile.displayPoints == form_data['make_my_points_public'] and \
            actual_profile.displayPurchases == form_data['make_my_purchases_public']

        self.assertTrue(profile_correct, msg="Expected the right user to be made if all the fields are valid, but failed.")

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
            'last_name': 'Knope',
            'email': 'lknope@pawnee.com'
        }

        form = ProfileCreateForm(data=form_data)
        self.assertFalse(form.is_valid(), msg="Expected the form to be invalid with missing data, but it was marked valid.")

class MessageSendTests(TestCase):
    # TODO: need to write after implementation
    pass

# Model Tests
class ProfileModelTests(TestCase):
    #TODO: write tests
    pass

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
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
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
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
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
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
        convo = create_convo("mscott-dschrute", [profile1, profile2])
        _ = create_message(profile1, convo, "Hi Dwight!")

        self.client.force_login(profile1.user)

        response = self.client.get(reverse('conversation', args=[convo.id]))
        self.assertQuerysetEqual(
            response.context['members'],
            [profile2.user.get_full_name(), profile1.user.get_full_name()],
            msg=f"Expected the members in a conversation with name {convo.name} to be returned when {profile1.user.username} is logged in, but failed."
        )

    def test_convo_several_messages_msgs_returned(self):
        """Tests that the right messages are returned from a conversation with multiple messages."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
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

class InboxViewTests(TestCase):
    def test_inbox_no_display_no_convos(self):
        """Tests that no conversations are rendered when none exist for a user."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)

        response = self.client.get(reverse('inbox'))
        self.assertQuerysetEqual(
            response.context['convos'],
            [],
            msg=f"Expected no conversation to be returned when logged in but none exist, but failed."
        )

    def test_inbox_no_display_not_logged_in(self):
        """Tests that no conversations are rendered when a user isn't logged in."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
        _ = create_convo("mscott-dschrute", [profile1, profile2])

        response = self.client.get(reverse('inbox'))
        self.assertQuerysetEqual(
            response.context['convos'],
            [],
            msg=f"Expected no conversation to be returned when not logged in, but failed."
        )

    def test_inbox_one_convo_two_users(self):
        """Tests that a conversation between two users is shown when one user is logged in."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
        convo = create_convo("mscott-dschrute", [profile1, profile2])

        self.client.force_login(profile1.user)

        response = self.client.get(reverse('inbox'))
        self.assertQuerysetEqual(
            response.context['convos'],
            [convo],
            msg=f"Expected a conversation with name {convo.name} to be returned when {profile1.user.username} is logged in, but failed."
        )

    def test_inbox_one_convo_two_users(self):
        """Tests that a conversation between two users is shown when the other user is logged in."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
        convo = create_convo("mscott-dschrute", [profile1, profile2])

        self.client.force_login(profile2.user)

        response = self.client.get(reverse('inbox'))
        self.assertQuerysetEqual(
            response.context['convos'],
            [convo],
            msg=f"Expected a conversation with name {convo.name} to be returned when {profile2.user.username} is logged in, but failed."
        )

    def test_inbox_multiple_convos(self):
        """Tests that three conversations are shown in order of most recent to least recent when the user is logged in."""
        profile1 = create_profile("mscott", "Michael", "Scott", True, 0)
        profile2 = create_profile("dschrute", "Dwight", "Schrute", False, 0)
        profile3 = create_profile("jhalpert", "Jim", "Halpert", True, 100)
        profile4 = create_profile("pbeasly", "Pam", "Beasly", True, 200)

        convo1 = create_convo("mscott-dschrute", [profile1, profile2])
        convo2 = create_convo("mscott-jhalpert", [profile1, profile3])
        convo3 = create_convo("mscott-pbeasly", [profile1, profile4])

        self.client.force_login(profile1.user)

        response = self.client.get(reverse('inbox'))
        self.assertQuerysetEqual(
            response.context['convos'],
            [convo3, convo2, convo1],
            msg=f"Expected three conversations to be returned when {profile1.user.username} is logged in, but failed."
        )

class LeaderboardViewTests(TestCase):
    def test_leaderboard_no_users(self):
        """Tests that the leaderboard displays no profiles when none exist."""
        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(response.context['users'], [], msg="Leaderboard displays profiles when none were expected.")

    def test_leaderboard_one_user_private(self):
        """Tests that the leaderboard displays no profiles when one has private data."""
        _ = create_profile("jsmith", "John", "Smith", display_points=False, points=10)

        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(response.context['users'], [], msg=f"Leaderboard displayed {response.context['users']}, when no public users were expected.")
    
    def test_leaderboard_one_user_public(self):
        """Tests that the leaderboard displays the sole profile with public data."""
        profile = create_profile("jsmith", "John", "Smith", True, 10)
        user_full_name = get_user_full_name(profile)
        expected_user_data = [(user_full_name, profile.points)]

        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(
            response.context['users'],
            expected_user_data,
            msg=f"Leaderboard displayed {response.context['users']}, when only one public user was expected: {expected_user_data}."
        )

    def test_leaderboard_several_users_mix(self):
        """Tests that the leaderboard only shows public profiles and orders them by points descending."""
        public1 = create_profile("public1", "Public", "One", display_points=True, points=10)
        public2 = create_profile("public2", "Public", "Two", display_points=True, points=20)
        _ = create_profile("private1", "Private", "One", display_points=False, points=30)
        
        expected_user_data = [(get_user_full_name(public2), public2.points), (get_user_full_name(public1), public1.points)]

        response = self.client.get(reverse('leaderboard'))
        self.assertQuerysetEqual(
            response.context['users'],
            expected_user_data,
            msg=f"Leaderboard displayed {response.context['users']}, when only the public profiles {expected_user_data} were expected."
        )

    def test_leaderboard_several_users_overflow(self):
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
            expected_user_data,
            msg=f"Leaderboard displayed {len(response.context['users'])} when only {NUM_USERS_TO_SHOW} were expected."
        )
