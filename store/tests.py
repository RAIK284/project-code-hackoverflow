from django.test import TestCase

# View Tests
class BuyViewTests(TestCase):
    def test_buy_view_shows_current_product_only(self):
        """Tests that the buy view shows only one product."""
        pass

    def test_buy_page_view_can_buy_with_enough_tokens(self):
        """Tests that the user can buy a product when they enough tokens."""
        pass

    def test_buy_page_view_buy_adds_to_user_purchases(self):
        """Tests that when the user buys a product, it's tied to their account."""
        pass

    def test_buy_page_view_cant_buy_duplicate(self):
        """Tests that a user can't buy a product they already own."""
        pass

    def test_buy_page_view_not_enough_tokens(self):
        """Tests that a user can't buy a product they can't afford."""
        pass

    def test_buy_page_view_update_product_purchase_count(self):
        """Tests that, once a product is bought, the number bought increases."""
        pass
