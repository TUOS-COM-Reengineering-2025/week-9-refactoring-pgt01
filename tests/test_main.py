import unittest
import io
import contextlib

from main import CustomerManager, calculate_shipping_fee_for_fragile_items

class TestCustomerManager(unittest.TestCase):

    def test_add_customer(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_customer(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_add_purchase(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase]},
            cm.customers
        )

    def test_add_purchases(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'},{'price': 20, 'item': 'pear'},{'price': 10, 'item': 'avocado'}]
        cm.add_purchases(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )
    def test_add_purchase_multiple(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase, purchase]},
            cm.customers
        )

    def test_discount_eligibility(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 600}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("Eligible for discount", output)

    def test_heavy_item_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 100, 'weight': 25}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 50)

    def test_fragile_item_shipping_fee(self):
        purchases = [{'price': 70, 'fragile': True}]

        fee = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee, 60)

    def test_no_special_items_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 40, 'weight': 5, 'fragile': False}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 20)

        fee_fragile = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee_fragile, 25)

    def test_generate_report_comprehensive(self):
        cm = CustomerManager()
        # Customer with no discount (total < 300)
        cm.add_customer("Alice", [{'price': 50}, {'price': 75}])

        # Customer with potential future discount (300 < total < 500)
        cm.add_customer("Charlie", [{'price': 350}])

        # Customer eligible for discount (total > 500)
        cm.add_customer("David", [{'price': 520}])

        # Customer eligible for discount and Priority (800 < total < 1000)
        cm.add_customer("Eve", [{'price': 850}])

        # VIP customer (total > 1000)
        cm.add_customer("Frank", [{'price': 1200}])

        # Priority customer (total > 1000)
        cm.add_customer("Jules", [{'price': 700}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        # Check each customer's status in the report
        self.assertIn("Alice", output)
        self.assertIn("No discount", output)

        self.assertIn("Charlie", output)
        self.assertIn("Potential future discount customer", output)

        self.assertIn("David", output)
        self.assertIn("Eligible for discount", output)

        self.assertIn("Eve", output)
        self.assertIn("Eligible for discount", output)

        self.assertIn("Frank", output)
        self.assertIn("Eligible for discount", output)
        self.assertIn("VIP Customer!", output)

if __name__ == "__main__":
    unittest.main()