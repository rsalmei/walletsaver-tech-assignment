import factory
from faker import Factory

from plans.models import CarrierPlan

faker = Factory.create()


class CarrierPlanFactory(factory.DjangoModelFactory):
    class Meta:
        model = CarrierPlan

    carrier = factory.LazyFunction(faker.random_digit)
    title = factory.LazyFunction(faker.word)
    description = factory.LazyFunction(faker.text)
    current_price = factory.LazyFunction(lambda: faker.random_number(digits=5) / 100)
    old_price = factory.LazyAttribute(lambda self: self.current_price * 1.1)
