from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from numpy import exp

from .models import Product, Purchase
from messaging.models import Profile

# Helper Functions
def create_product(name: str, cost: int, amt_sold: int=0) -> Product:
    """
    Helper function to create a product.

    :param name - the name of the product
    :param cost - the point cost of the product
    :param amt_sold - the number of users who bought the product (optional)
    :return the product
    """
    return Product.objects.create(name=name, point_cost=cost, amount_sold=amt_sold)

def create_profile(username: str, first_name: str, last_name: str, wallet: int=0, password: str='YuR46aeZR', email: str='user@email.com') -> Profile:
    """
    Helper function that creates a profile for a user.

    :param username - the username to use
    :param first_name - user's first name
    :param last_name - user's last name
    :param wallet - the number of points the user can spend
    :param password - (optional) the user's password
    :param email - (optional) the user's email
    :return the created Profile
    """
    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    return Profile.objects.create(user=user, wallet=wallet) 

# View Tests
class IndexViewTests(TestCase):
    def test_index_view_shows_all_products(self):
        """Tests that the index view shows all the expected products, in order of popularity"""
        expected_products = []
        for i in range(5):
            expected_products.append(create_product(f"Product {i}", 1, amt_sold=i))

        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['products'],
            list(reversed(expected_products)),
            msg="Expected products to be displayed in order of popularity, but failed."
        )

class BuyViewTests(TestCase):
    def test_buy_view_shows_current_product_only(self):
        """Tests that the buy view shows only one product."""
        profile = create_profile("mscott", "Michael", "Scott")
        expected_product = create_product('test product', 1)

        self.client.force_login(profile.user)
        response = self.client.get(reverse('buy', args=[expected_product.id]))
        self.assertEquals(
            response.context['product'],
            expected_product,
            "Expected the correct product to be displayed on its buy page, but it wasn't."
        )

    def test_buy_page_view_can_buy_with_enough_tokens(self):
        """Tests that the user can buy a product when they enough tokens."""
        expected_wallet = 9
        profile = create_profile("mscott", "Michael", "Scott", expected_wallet + 1)
        product = create_product('test product', 1)

        self.client.force_login(profile.user)
        _ = self.client.get(reverse('buy_page', args=[product.id]))
        profile.refresh_from_db()
        self.assertEquals(
            profile.wallet,
            expected_wallet,
            "Expected the product to be bought when the user has enough tokens, but it didn't."
        )

    def test_buy_page_view_buy_adds_to_user_purchases(self):
        """Tests that when the user buys a product, it's tied to their account."""
        profile = create_profile("mscott", "Michael", "Scott", 10)
        expected_product = create_product('test product', 1)

        self.client.force_login(profile.user)
        _ = self.client.get(reverse('buy_page', args=[expected_product.id]))
        profile.refresh_from_db()

        actual_product = Purchase.objects.get(buyer=profile).product

        self.assertEquals(
            expected_product,
            actual_product,
            "Expected the product to be bought and a Purchase to be created when the user has enough tokens, but it didn't."
        )

    def test_buy_page_view_cant_buy_duplicate(self):
        """Tests that a user can't buy a product they already own."""
        expected_wallet = 9
        profile = create_profile("mscott", "Michael", "Scott", expected_wallet + 1)
        product = create_product('test product', 1)

        self.client.force_login(profile.user)
        _ = self.client.get(reverse('buy_page', args=[product.id]))
        profile.refresh_from_db()

        # Buy again!
        _ = self.client.get(reverse('buy_page', args=[product.id]))
        profile.refresh_from_db()

        self.assertEquals(
            profile.wallet,
            expected_wallet,
            "Expected the product to only be able to be bought once by a user, but it failed."
        )

    def test_buy_page_view_not_enough_tokens(self):
        """Tests that a user can't buy a product they can't afford."""
        profile = create_profile("mscott", "Michael", "Scott", 0)
        product = create_product('test product', 1)

        self.client.force_login(profile.user)
        _ = self.client.get(reverse('buy_page', args=[product.id]))
        product.refresh_from_db()

        self.assertEquals(
            product.amount_sold,
            0,
            "Expected the product to not be bought if the user doesn't have enough points, but it failed."
        )

    def test_buy_page_view_update_product_purchase_count(self):
        """Tests that, once a product is bought, the number bought increases."""
        profile = create_profile("mscott", "Michael", "Scott", 10)
        product = create_product('test product', 1)

        self.client.force_login(profile.user)
        _ = self.client.get(reverse('buy_page', args=[product.id]))
        product.refresh_from_db()

        self.assertEquals(
            product.amount_sold,
            1,
            "Expected the product to increment its amount sold when sold successfully, but it failed."
        )
