"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger, FuzzyFloat
from service.models import Shopcart

class ItemFactory(factory.Factory):
    """Creates fake items in shopcarts that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Shopcart
    
    user_id = factory.Sequence(lambda n: n)
    item_id = FuzzyInteger(0)
    item_name = "ring" + str(item_id)
    quantity = FuzzyInteger(0, 999)
    price = FuzzyFloat(0.1)